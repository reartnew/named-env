"""Variables definition"""

import os
import typing as t

from .exceptions import (
    MissingVariableError,
    ChoiceValueError,
)
from .namespace import EnvironmentNamespace

__all__ = [
    "BaseVariableMixin",
    "RequiredVariableMixin",
    "OptionalVariableMixin",
    "RequiredString",
    "RequiredFloat",
    "RequiredInteger",
    "RequiredBoolean",
    "OptionalString",
    "OptionalFloat",
    "OptionalInteger",
    "OptionalBoolean",
    "RequiredList",
    "OptionalList",
]

sentinel = object()


class BaseVariableMixin:
    """Common ancestor for all variables classes"""

    _choice: t.Optional[t.Sequence] = None

    def __set_name__(self, owner: type, name: str):
        self._name: t.Optional[str] = name
        self._namespace = owner if issubclass(owner, EnvironmentNamespace) else None

    def __get__(self, obj, objtype=None):
        namespace: t.Union[t.Type[EnvironmentNamespace], EnvironmentNamespace, None] = (
            obj
            if isinstance(obj, EnvironmentNamespace)
            else objtype
            if issubclass(objtype, EnvironmentNamespace)
            else None
        )
        if self._value is sentinel or namespace is not None and not namespace.cache_values:
            env = (namespace or os).environ
            if self._name in env:
                self._set_value(env[self._name])
            elif isinstance(self, OptionalVariableMixin):
                self._set_value(self.default)
            elif isinstance(self, RequiredVariableMixin):
                raise MissingVariableError(variable=self._name, description=self.description)
        return self._value

    def _set_value(self, value: t.Any) -> None:
        """Cast-check-set"""
        cast_value: t.Any = self.cast(value)
        self._validate_cast_value(cast_value)
        self._value = cast_value

    def _validate_cast_value(self, cast_value: t.Any) -> None:
        if self._choice is not None and cast_value not in self._choice:
            raise ChoiceValueError(f"{self._name} variable has an unexpected value")

    @classmethod
    def _get_base_class(cls) -> type:
        """Find first non-BaseVariableMixin superclass"""
        for klass in cls.mro():
            if not issubclass(klass, BaseVariableMixin):
                return klass
        raise TypeError(f"Non-BaseVariableMixin superclass not found for {cls}")

    def __new__(cls, *args, **kwargs) -> t.Any:
        choice: t.Optional[t.Sequence] = kwargs.pop("choice", None)
        if choice is not None and not isinstance(choice, t.Sequence):
            raise ValueError(f"'choice' argument must be a sequence (got {type(choice)!r})")
        obj = cls._get_base_class().__new__(cls, *args, **kwargs)  # noqa
        obj._choice = choice
        obj._name = None
        obj._namespace = None
        obj._value = sentinel
        return obj

    @classmethod
    def cast(cls, value):
        """Transform environment string value into desired type"""
        return cls._get_base_class()(value)


class RequiredVariableMixin(BaseVariableMixin):
    """Required variables with optional description to inform on failed obtaining"""

    # pylint: disable=unused-argument
    def __init__(self, *, description: t.Optional[str] = None, choice: t.Optional[t.Sequence] = None) -> None:
        self.description = description


class OptionalVariableMixin(BaseVariableMixin):
    """Optional variables with required default value"""

    # pylint: disable=unused-argument
    def __init__(self, default: t.Any, choice: t.Optional[t.Sequence] = None) -> None:
        self.default = default


class Boolean(BaseVariableMixin):
    """Bool-like class to interpret string values"""

    _POSITIVE_VALUES: t.Set[str] = {"y", "yes", "true", "1"}
    _NEGATIVE_VALUES: t.Set[str] = {"n", "no", "false", "0", "none"}

    @classmethod
    def cast(cls, value) -> t.Optional[bool]:
        """Override default cast to produce pure booleans"""
        normalized_value: t.Optional[str] = str(value).lower()
        return (
            False
            if normalized_value in cls._NEGATIVE_VALUES
            else True
            if normalized_value in cls._POSITIVE_VALUES
            else None
        )

    def __new__(cls, *args, **kwargs) -> t.Any:
        if "choice" in kwargs:
            raise TypeError(f"{cls.__name__}.__new__() got an unexpected keyword argument 'choice'")
        kwargs["choice"] = [True, False]
        return super().__new__(cls, *args, **kwargs)


class List(BaseVariableMixin, list):
    """Comma-separated lists reading"""

    @classmethod
    def cast(cls, value: t.Union[t.List[str], str]) -> t.List[str]:
        return [item.strip() for item in value.split(",") if item] if isinstance(value, str) else value

    def _validate_cast_value(self, cast_value: t.Any) -> None:
        for cast_value_item in cast_value:  # type: t.Any
            super()._validate_cast_value(cast_value_item)


class RequiredString(RequiredVariableMixin, str):
    """String-like required variable class"""


class RequiredFloat(RequiredVariableMixin, float):
    """Float-like required variable class"""


class RequiredInteger(RequiredVariableMixin, int):
    """Integer-like required variable class"""


class RequiredBoolean(RequiredVariableMixin, Boolean):
    """Boolean-like required variable class"""


class OptionalString(OptionalVariableMixin, str):
    """String-like optional variable class"""


class OptionalFloat(OptionalVariableMixin, float):
    """Float-like optional variable class"""


class OptionalInteger(OptionalVariableMixin, int):
    """Integer-like optional variable class"""


class OptionalBoolean(OptionalVariableMixin, Boolean):
    """Boolean-like optional variable class"""


class RequiredList(RequiredVariableMixin, List):
    """List-like required variable class"""


class OptionalList(OptionalVariableMixin, List):
    """List-like optional variable class"""
