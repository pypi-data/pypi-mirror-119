__all__ = [
    'VariantRegistry',
    'attribute',
    'fix_attrs_converters',
    'BaseTolokaObjectMetaclass',
    'BaseTolokaObject'
]

import inspect
import typing
from copy import copy
from enum import Enum
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar, Union

import attr

from .._converter import converter
from ..exceptions import SpecClassIdentificationError

REQUIRED_KEY = 'toloka_field_required'
ORIGIN_KEY = 'toloka_field_origin'
READONLY_KEY = 'toloka_field_readonly'
AUTOCAST_KEY = 'toloka_field_autocast'

E = TypeVar('E', bound=Enum)


class VariantRegistry:

    def __init__(self, field: str, enum: Type[E]):
        self.field: str = field
        self.enum: Type[E] = enum
        self.registered_classes: Dict[E, type] = {}

    def register(self, type_: type, value: E) -> type:

        if not isinstance(value, self.enum):
            raise TypeError(f'spec_value must be an instance of {self.enum} not {value}')

        if value in self.registered_classes:
            raise TypeError(f'Specification for {value} is already registered')

        setattr(type_, self.field, value)
        self.registered_classes[value] = type_

        return type_

    def __getitem__(self, value: E):
        return self.registered_classes[value]


def attribute(*args, required: bool = False, origin: Optional[str] = None, readonly: bool = False,
              autocast: bool = False, **kwargs):
    """Proxy for attr.attrib(...). Adds several keywords.

    Args:
        *args: All positional arguments from attr.attrib
        required: If True makes attribute not Optional. All other attributes are optional by default. Defaults to False.
        origin: Sets field name in dict for attribute, when structuring/unstructuring from dict. Defaults to None.
        readonly: Affects only when the class 'expanding' as a parameter in some function. If True, drops this attribute from expanded parameters. Defaults to None.
        autocast: If True then converter.structure will be used to convert input value
        **kwargs: All keyword arguments from attr.attrib
    """
    metadata = {}
    if required:
        metadata[REQUIRED_KEY] = True
    if origin:
        metadata[ORIGIN_KEY] = origin
    if readonly:
        metadata[READONLY_KEY] = True
    if autocast:
        metadata[AUTOCAST_KEY] = True
    return attr.attrib(*args, metadata=metadata, **kwargs)


def get_autocast_converter(type_):
    def autocast_converter(value: enum_type_to_union(type_)):
        return converter.structure(value, type_)

    return autocast_converter


def enum_type_to_union(cur_type):
    if cur_type.__module__ == 'typing':
        if not hasattr(cur_type, '__args__') or not hasattr(cur_type, '__origin__'):
            return cur_type

        origin = cur_type.__origin__
        # starting from python 3.7 origin of generic types returns true type instead of typing generic (i.e.
        # typing.List[int].__origin__ == list) but using types as type hints directly supported only in python >= 3.9
        if origin.__module__ != 'typing':
            origin = getattr(typing, origin.__name__.title())

        return origin[tuple(map(enum_type_to_union, cur_type.__args__))]
    elif inspect.isclass(cur_type) and issubclass(cur_type, Enum):
        possible_types = set(type(item.value) for item in cur_type)
        return typing.Union[(cur_type, *possible_types)] if possible_types else cur_type
    else:
        return cur_type


def fix_attrs_converters(cls):
    """
    Due to https://github.com/Toloka/toloka-kit/issues/37 we have to support attrs>=20.3.0.
    This version lacks a feature that uses converters' annotations in class's __init__
    (see https://github.com/python-attrs/attrs/pull/710)). This decorator brings this feature
    to older attrs versions.
    """

    if attr.__version__ < '21.0.3':
        fields_dict = attr.fields_dict(cls)

        def update_param_from_converter(param):

            # Trying to figure out which attribute this parameter is responsible for.
            # Note that attr stips leading underscores from attribute names, so we
            # check both name and _name.
            attribute = fields_dict.get(param.name) or fields_dict.get('_' + param.name)

            # Only process attributes with converter
            if attribute is not None and attribute.converter:
                # Retrieving converter's first (and only) parameter
                converter_sig = inspect.signature(attribute.converter)
                converter_param = next(iter(converter_sig.parameters.values()))
                # And use this parameter's annotation for our own
                param = param.replace(annotation=converter_param.annotation)

            return param

        init_sig = inspect.signature(cls.__init__)
        new_params = [update_param_from_converter(param) for param in init_sig.parameters.values()]
        new_annotations = {param.name: param.annotation for param in new_params if param.annotation}
        cls.__init__.__signature__ = init_sig.replace(parameters=new_params)
        cls.__init__.__annotations__ = new_annotations

    return cls


class BaseTolokaObjectMetaclass(type):

    def __new__(mcs, name, bases, namespace, auto_attribs=True, kw_only=True, frozen=False, order=True, eq=True,
                **kwargs):
        cls = attr.attrs(
            auto_attribs=auto_attribs,
            kw_only=kw_only,
            field_transformer=mcs.transformer,
            frozen=frozen,
            order=order,
            eq=eq,
            str=True,
            collect_by_mro=True,
        )(super().__new__(mcs, name, bases, namespace, **kwargs))

        cls = fix_attrs_converters(cls)

        # Transformer's change in field type does not affect created
        # class's annotations. So we synchronize them manually
        annotations = getattr(cls.__dict__, '__annotations__', {})
        for field in attr.fields(cls):
            if field.type is not None:
                annotations[field.name] = field.type
        cls.__annotations__ = annotations

        return cls

    @staticmethod
    def transformer(type_: type, fields: List[attr.Attribute]) -> List[attr.Attribute]:
        transformed_fields = []

        for field in fields:
            # Make all attributes optional unless explicitly configured otherwise
            if not field.metadata.get(REQUIRED_KEY):
                field = field.evolve(
                    type=Optional[field.type] if field.type else field.type,
                    default=None if field.default is attr.NOTHING else field.default,
                )

            if field.metadata.get(AUTOCAST_KEY):
                field = field.evolve(
                    converter=get_autocast_converter(field.type),
                    on_setattr=lambda self, attrib, value, type_=field.type: converter.structure(value, type_),
                )

            transformed_fields.append(field)

        return transformed_fields


class BaseTolokaObject(metaclass=BaseTolokaObjectMetaclass):
    """
    A base class for classes representing Toloka objects.



    Subclasses of BaseTolokaObject will:
    * Automatically convert annotated attributes attributes via attrs making them optional
      if not explicitly configured otherwise
    * Skip missing optional fields during unstructuring with client's cattr converter
    """

    _variant_registry: ClassVar[Optional[VariantRegistry]] = None
    _unexpected: Dict[str, Any] = attribute(factory=dict, init=False)

    def __new__(cls, *args, **kwargs):
        """Overriding new for our check to be executed before auto-generated __init__"""
        if cls.is_variant_incomplete():
            message = 'Cannot instantiate an incomplete variant type on field {}'
            raise TypeError(message.format(cls._variant_registry.field))

        return super().__new__(cls)

    @classmethod
    def __init_subclass__(cls, spec_enum: Optional[Union[str, Type[E]]] = None,
                          spec_field: Optional[str] = None, spec_value=None):

        # Completing a variant type
        if spec_value is not None:
            cls._variant_registry.register(cls, spec_value)

        # Making into a variant type
        if spec_enum is not None or spec_field is not None:

            if spec_enum is None or spec_field is None:
                raise ValueError('Both spec_enum and spec_field must be provided')

            if cls.is_variant_incomplete():
                message = 'Incomplete variant type on field {} cannot be a variant type itself'
                raise TypeError(message.format(cls._variant_registry.field))

            # TODO: Possibly make it immutable
            enum = getattr(cls, spec_enum) if isinstance(spec_enum, str) else spec_enum
            cls._variant_registry = VariantRegistry(spec_field, enum)

    # Unexpected fields access

    def __getattr__(self, item):
        try:
            # get _unexpected pickle-friendly
            _unexpected = super().__getattribute__('_unexpected')
            return _unexpected[item]
        except KeyError as exc:
            raise AttributeError(str(item)) from exc

    # Variant type related checks

    @classmethod
    def is_variant_base(cls) -> bool:
        return '_variant_registry' in cls.__dict__

    @classmethod
    def is_variant_incomplete(cls) -> bool:
        return cls._variant_registry and cls._variant_registry.field not in cls.__dict__  # type: ignore

    @classmethod
    def is_variant_spec(cls) -> bool:
        return cls._variant_registry and cls._variant_registry.field in cls.__dict__  # type: ignore

    @classmethod
    def get_variant_specs(cls) -> dict:
        variant_specs = {}
        for base in cls.__mro__:
            registry = base.__dict__.get('_variant_registry')
            if registry:
                variant_specs[registry.field] = getattr(cls, registry.field)

        return variant_specs

    @classmethod
    def get_spec_subclass_for_value(cls, spec_value: Union[str, E] = None) -> type:
        try:
            spec_value = cls._variant_registry.enum(spec_value)
        except ValueError:
            return None
        return cls._variant_registry[spec_value]

    # Conversions related functions

    def unstructure(self) -> Optional[dict]:
        data = dict(self._unexpected)
        obj_class = type(self)

        for field in attr.fields(obj_class):
            if field.name == '_unexpected':
                continue

            value = converter.unstructure(getattr(self, field.name))
            if field.metadata.get(REQUIRED_KEY) or value is not None:
                key = field.metadata.get(ORIGIN_KEY, field.name)
                data[key] = value

        data.update(converter.unstructure(self.get_variant_specs()))
        assert '_unexpected' not in data
        return data or None

    @classmethod
    def structure(cls, data: dict):

        # If a class is an incomplete variant type we structure it into
        # one of its subclasses
        if cls.is_variant_incomplete():
            # TODO: Optimize copying
            data = dict(data)  # Do not modify input data
            spec_field = cls._variant_registry.field
            data_field = data.pop(spec_field)
            try:
                spec_value = cls._variant_registry.enum(data_field)
                spec_class = cls._variant_registry.registered_classes[spec_value]
            except Exception:
                raise SpecClassIdentificationError(spec_field=spec_field,
                                                   spec_enum=cls._variant_registry.enum.__name__)
            return spec_class.structure(data)

        data = copy(data)
        kwargs = {}

        for field in attr.fields(cls):
            key = field.metadata.get(ORIGIN_KEY, field.name)
            if key not in data:
                continue

            value = data.pop(key)
            if field.type is not None:
                value = converter.structure(value, field.type)

            kwargs[field.name] = value

        obj = cls(**kwargs)
        obj._unexpected = data
        return obj
