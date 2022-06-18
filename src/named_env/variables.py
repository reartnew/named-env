"""Variables definition"""

import typing as t

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
]


class BaseVariableMixin:
    """Common ancestor for all variables classes"""

    @classmethod
    def _get_base_class(cls) -> type:
        # Find first non-BaseVariable superclass
        for klass in cls.mro():
            if not issubclass(klass, BaseVariableMixin):
                return klass
        raise TypeError(f"Non-BaseVariable superclass not found for {cls}")

    def __new__(cls, *args, **kwargs) -> t.Any:
        return cls._get_base_class().__new__(cls, *args, **kwargs)

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
    """Bool-like class to interpret string values. Can't subclass ```bool``` directly."""

    _POSITIVE: t.Set[str] = {"y", "yes", "true"}
    _NEGATIVE: t.Set[str] = {"n", "no", "false"}

    def __init__(self, value: t.Union[str, bool, None] = None) -> None:
        normalized_value: t.Optional[str] = str(value).lower() if value is not None else None
        assert normalized_value in self._POSITIVE | self._NEGATIVE | {
            None
        }, f"{repr(value)} is not a valid bool-convertible value"
        self._value = normalized_value

    def __bool__(self) -> bool:
        assert self._value is not None, "Expected late init"
        return self._value in self._POSITIVE

    @classmethod
    def cast(cls, value) -> bool:
        """Override default cast to produce pure booleans"""
        return bool(value)


class RequiredString(str, RequiredVariableMixin):
    """String-like required variable class"""


class RequiredFloat(float, RequiredVariableMixin):
    """Float-like required variable class"""


class RequiredInteger(int, RequiredVariableMixin):
    """Integer-like required variable class"""


class RequiredBoolean(Boolean, RequiredVariableMixin):
    """Boolean-like required variable class"""


class OptionalString(str, OptionalVariableMixin):
    """String-like optional variable class"""


class OptionalFloat(float, OptionalVariableMixin):
    """Float-like optional variable class"""


class OptionalInteger(int, OptionalVariableMixin):
    """Integer-like optional variable class"""


class OptionalBoolean(Boolean, OptionalVariableMixin):
    """Boolean-like optional variable class"""
