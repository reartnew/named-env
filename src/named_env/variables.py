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
        return cls._get_base_class().__new__(cls, *args, **kwargs)  # noqa

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
    _NEGATIVE_VALUES: t.Set[str] = {"n", "no", "false", "0"}

    def __init__(self, value: t.Union[str, bool, None] = None) -> None:
        self._value = value

    def __bool__(self) -> bool:
        assert self._value is not None, "Expected late init"
        return self._value in self._POSITIVE_VALUES

    @classmethod
    def cast(cls, value) -> bool:
        """Override default cast to produce pure booleans"""
        normalized_value: t.Optional[str] = str(value).lower() if value is not None else None
        if normalized_value not in cls._POSITIVE_VALUES | cls._NEGATIVE_VALUES | {None}:
            raise ValueError(f"{repr(value)} is not a valid bool-convertible value")
        return bool(value)


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
