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
    BAD_INTEGER = RequiredInteger()
    BAD_FLOAT = RequiredFloat()
    BAD_BOOLEAN = RequiredBoolean()
    REQUIRED_STRING_TO_SET = RequiredString()
    REQUIRED_INTEGER_TO_SET = RequiredInteger()
    REQUIRED_BUT_MISSING_INTEGER_TO_SET = RequiredInteger()
    REQUIRED_FLOAT_TO_SET = RequiredFloat()
    OPTIONAL_STRING_TO_SET = OptionalString("OPTIONAL_STRING_TO_SET value before set")


constants = PytestEnvironmentNamespace(
    env_source=dict(
        REQUIRED_DEFINED_STRING="REQUIRED_DEFINED_STRING defined value",
        OPTIONAL_DEFINED_STRING="OPTIONAL_DEFINED_STRING defined value",
        GOOD_INTEGER="1",
        GOOD_FLOAT="10.",
        GOOD_BOOLEAN="N",
        BAD_INTEGER="Foo",
        BAD_FLOAT="Bar",
        BAD_BOOLEAN="Baz",
        REQUIRED_STRING_TO_SET="REQUIRED_STRING_TO_SET value before set",
        REQUIRED_INTEGER_TO_SET="Not even an integer",
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


def test_good_int():
    """Check integer cast"""
    assert isinstance(constants.GOOD_INTEGER, int)
    assert constants.GOOD_INTEGER == 1


def test_good_float():
    """Check float cast"""
    assert isinstance(constants.GOOD_FLOAT, float)
    assert constants.GOOD_FLOAT == 10.0


def test_good_bool():
    """Check boolean cast"""
    assert isinstance(constants.GOOD_BOOLEAN, bool)
    assert not constants.GOOD_BOOLEAN


def test_bad_int():
    """Check integer cast failure"""
    with pytest.raises(ValueError, match="invalid literal for int"):
        assert constants.BAD_INTEGER


def test_bad_float():
    """Check float cast failure"""
    with pytest.raises(ValueError, match="could not convert string to float"):
        assert constants.BAD_FLOAT


def test_bad_bool():
    """Check boolean cast failure"""
    with pytest.raises(ValueError, match="is not a valid bool-convertible value"):
        assert constants.BAD_BOOLEAN is False


# pylint: disable=invalid-name
def test_required_string_set():
    """Check set operation on required strings"""
    assert constants.REQUIRED_STRING_TO_SET == "REQUIRED_STRING_TO_SET value before set"
    constants.REQUIRED_STRING_TO_SET = "REQUIRED_STRING_TO_SET value after set"
    assert constants.REQUIRED_STRING_TO_SET == "REQUIRED_STRING_TO_SET value after set"


# pylint: disable=invalid-name
def test_optional_string_set():
    """Check set operation on optional strings"""
    assert constants.OPTIONAL_STRING_TO_SET == "OPTIONAL_STRING_TO_SET value before set"
    constants.OPTIONAL_STRING_TO_SET = "OPTIONAL_STRING_TO_SET value after set"
    assert constants.OPTIONAL_STRING_TO_SET == "OPTIONAL_STRING_TO_SET value after set"


# pylint: disable=invalid-name
def test_bad_integer_good_set():
    """Validate good set operation over bad values"""
    constants.REQUIRED_INTEGER_TO_SET = 2
    assert constants.REQUIRED_INTEGER_TO_SET == 2


# pylint: disable=invalid-name
def test_missing_integer_good_set():
    """Validate good set operation over missing values"""
    constants.REQUIRED_BUT_MISSING_INTEGER_TO_SET = 3
    assert constants.REQUIRED_BUT_MISSING_INTEGER_TO_SET == 3


# pylint: disable=invalid-name
def test_float_bad_set():
    """Validate bad set operation"""
    with pytest.raises(ValueError, match="could not convert string to float"):
        constants.REQUIRED_FLOAT_TO_SET = "FooBar"
