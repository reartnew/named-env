"""Variables definition"""

import os
import typing as t

from .exceptions import MissingVariableError
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

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if self._value is sentinel:
            env = (
                obj.environ
                if isinstance(obj, EnvironmentNamespace)
                else objtype.environ
                if issubclass(objtype, EnvironmentNamespace)
                else os.environ
            )
            if self._name in env:
                self._value = self.cast(env[self._name])
            elif isinstance(self, OptionalVariableMixin):
                # Cast defaults also
                self._value = self.cast(self.default)
            elif isinstance(self, RequiredVariableMixin):
                raise MissingVariableError(variable=self._name, description=self.description)
        return self._value

    @classmethod
    def _get_base_class(cls) -> type:
        """Find first non-BaseVariableMixin superclass"""
        for klass in cls.mro():
            if not issubclass(klass, BaseVariableMixin):
                return klass
        raise TypeError(f"Non-BaseVariableMixin superclass not found for {cls}")

    def __new__(cls, *args, **kwargs) -> t.Any:
        obj = cls._get_base_class().__new__(cls, *args, **kwargs)  # noqa
        obj._name = None
        obj._value = sentinel
        return obj

    @classmethod
    def cast(cls, value):
        """Transform environment string value into desired type"""
        return cls._get_base_class()(value)


class RequiredVariableMixin(BaseVariableMixin):
    """Required variables with optional description to inform on failed obtaining"""

    def __init__(self, *, description: t.Optional[str] = None) -> None:
        self.description = description


class OptionalVariableMixin(BaseVariableMixin):
    """Optional variables with required default value"""

    def __init__(self, default: t.Any) -> None:
        self.default = default


class Boolean(BaseVariableMixin):
    """Bool-like class to interpret string values"""

    _POSITIVE_VALUES: t.Set[str] = {"y", "yes", "true", "1"}
    _NEGATIVE_VALUES: t.Set[str] = {"n", "no", "false", "0", "none"}

    @classmethod
    def cast(cls, value) -> bool:
        """Override default cast to produce pure booleans"""
        normalized_value: t.Optional[str] = str(value).lower()
        if normalized_value not in cls._POSITIVE_VALUES | cls._NEGATIVE_VALUES:
            raise ValueError(f"{repr(value)} is not a valid bool-convertible value")
        return normalized_value in cls._POSITIVE_VALUES


class List(BaseVariableMixin, list):
    """Comma-separated lists reading"""

    @classmethod
    def cast(cls, value: t.Union[t.List[str], str]) -> t.List[str]:
        return [item.strip() for item in value.split(",") if item] if isinstance(value, str) else value


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
