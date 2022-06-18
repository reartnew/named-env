"""EnvironmentNamespace tests"""
import pytest

from named_env import (
    EnvironmentNamespace,
    RequiredString,
    OptionalString,
    RequiredInteger,
    RequiredFloat,
    RequiredBoolean,
    MissingVariableError,
)


class PytestEnvironmentNamespace(EnvironmentNamespace):
    """Test environment"""

    REQUIRED_DEFINED_STRING = RequiredString()
    REQUIRED_UNDEFINED_STRING = RequiredString()
    OPTIONAL_DEFINED_STRING = OptionalString("OPTIONAL_DEFINED_STRING default value")
    OPTIONAL_UNDEFINED_STRING = OptionalString("OPTIONAL_UNDEFINED_STRING default value")
    GOOD_INTEGER = RequiredInteger()
    GOOD_FLOAT = RequiredFloat()
    GOOD_BOOLEAN = RequiredBoolean()


constants = PytestEnvironmentNamespace(
    env=dict(
        REQUIRED_DEFINED_STRING="REQUIRED_DEFINED_STRING defined value",
        OPTIONAL_DEFINED_STRING="OPTIONAL_DEFINED_STRING defined value",
        GOOD_INTEGER="1",
        GOOD_FLOAT="10.",
        GOOD_BOOLEAN="Y",
    )
)


def test_defined_required_string():
    """Check required defined string variable"""
    assert isinstance(constants.REQUIRED_DEFINED_STRING, str)
    assert constants.REQUIRED_DEFINED_STRING == "REQUIRED_DEFINED_STRING defined value"


def test_defined_optional_string():
    """Check optional defined string variable"""
    assert isinstance(constants.OPTIONAL_DEFINED_STRING, str)
    assert constants.OPTIONAL_DEFINED_STRING == "OPTIONAL_DEFINED_STRING defined value"


def test_undefined_required_string():
    """Check required undefined string variable"""
    with pytest.raises(MissingVariableError):
        assert constants.REQUIRED_UNDEFINED_STRING


def test_undefined_optional_string():
    """Check optional undefined string variable"""
    assert isinstance(constants.OPTIONAL_UNDEFINED_STRING, str)
    assert constants.OPTIONAL_UNDEFINED_STRING == "OPTIONAL_UNDEFINED_STRING default value"


def test_int():
    """Check integer cast"""
    assert isinstance(constants.GOOD_INTEGER, int)
    assert constants.GOOD_INTEGER == 1


def test_float():
    """Check float cast"""
    assert isinstance(constants.GOOD_FLOAT, float)
    assert constants.GOOD_FLOAT == 10.0


def test_bool():
    """Check boolean cast"""
    assert isinstance(constants.GOOD_BOOLEAN, bool)
    assert constants.GOOD_BOOLEAN
