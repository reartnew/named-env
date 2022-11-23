"""EnvironmentNamespace tests"""

import pytest

from named_env import (
    EnvironmentNamespace,
    RequiredString,
    OptionalString,
    RequiredInteger,
    RequiredFloat,
    RequiredBoolean,
    RequiredList,
    OptionalList,
    MissingVariableError,
)

# Test environment dict
environ = dict(
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
    REQUIRED_DEFINED_LIST="REQUIRED_DEFINED_LIST defined value",
    OPTIONAL_DEFINED_LIST="OPTIONAL_DEFINED_LIST defined value",
)


class PytestEnvironmentNamespace(EnvironmentNamespace):
    """Test environment namespace"""

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
    REQUIRED_BOOLEAN_TO_SET = RequiredBoolean()
    REQUIRED_DEFINED_LIST = RequiredList()
    REQUIRED_UNDEFINED_LIST = RequiredList()
    OPTIONAL_DEFINED_LIST = OptionalList(["OPTIONAL_DEFINED_LIST default value"])
    OPTIONAL_UNDEFINED_LIST = OptionalList(["OPTIONAL_UNDEFINED_LIST default value"])


def parametrized_constants_source(func):
    """Check both type-based and instance-based definitions"""

    class ConstantsClass(PytestEnvironmentNamespace):
        """Used for class-based (not instance-based) access tests"""

        environ = environ

    return pytest.mark.parametrize("constants", [PytestEnvironmentNamespace(environ=environ), ConstantsClass])(func)


@parametrized_constants_source
def test_defined_required_string(constants):
    """Check required defined string variable"""
    assert isinstance(constants.REQUIRED_DEFINED_STRING, str)
    assert constants.REQUIRED_DEFINED_STRING == "REQUIRED_DEFINED_STRING defined value"


@parametrized_constants_source
def test_defined_optional_string(constants):
    """Check optional defined string variable"""
    assert isinstance(constants.OPTIONAL_DEFINED_STRING, str)
    assert constants.OPTIONAL_DEFINED_STRING == "OPTIONAL_DEFINED_STRING defined value"


@parametrized_constants_source
def test_undefined_required_string(constants):
    """Check required undefined string variable"""
    with pytest.raises(MissingVariableError):
        assert constants.REQUIRED_UNDEFINED_STRING


@parametrized_constants_source
def test_undefined_optional_string(constants):
    """Check optional undefined string variable"""
    assert isinstance(constants.OPTIONAL_UNDEFINED_STRING, str)
    assert constants.OPTIONAL_UNDEFINED_STRING == "OPTIONAL_UNDEFINED_STRING default value"


@parametrized_constants_source
def test_good_int(constants):
    """Check integer cast"""
    assert isinstance(constants.GOOD_INTEGER, int)
    assert constants.GOOD_INTEGER == 1


@parametrized_constants_source
def test_good_float(constants):
    """Check float cast"""
    assert isinstance(constants.GOOD_FLOAT, float)
    assert constants.GOOD_FLOAT == 10.0


@parametrized_constants_source
def test_good_bool(constants):
    """Check boolean cast"""
    assert isinstance(constants.GOOD_BOOLEAN, bool)
    assert not constants.GOOD_BOOLEAN


@parametrized_constants_source
def test_bad_int(constants):
    """Check integer cast failure"""
    with pytest.raises(ValueError, match="invalid literal for int"):
        assert constants.BAD_INTEGER


@parametrized_constants_source
def test_bad_float(constants):
    """Check float cast failure"""
    with pytest.raises(ValueError, match="could not convert string to float"):
        assert constants.BAD_FLOAT


@parametrized_constants_source
def test_bad_bool(constants):
    """Check boolean cast failure"""
    with pytest.raises(ValueError, match="is not a valid bool-convertible value"):
        assert constants.BAD_BOOLEAN is False


@parametrized_constants_source
# pylint: disable=invalid-name
def test_required_string_set(constants):
    """Check set operation on required strings"""
    assert constants.REQUIRED_STRING_TO_SET == "REQUIRED_STRING_TO_SET value before set"
    constants.REQUIRED_STRING_TO_SET = "REQUIRED_STRING_TO_SET value after set"
    assert constants.REQUIRED_STRING_TO_SET == "REQUIRED_STRING_TO_SET value after set"


@parametrized_constants_source
# pylint: disable=invalid-name
def test_optional_string_set(constants):
    """Check set operation on optional strings"""
    assert constants.OPTIONAL_STRING_TO_SET == "OPTIONAL_STRING_TO_SET value before set"
    constants.OPTIONAL_STRING_TO_SET = "OPTIONAL_STRING_TO_SET value after set"
    assert constants.OPTIONAL_STRING_TO_SET == "OPTIONAL_STRING_TO_SET value after set"


@parametrized_constants_source
# pylint: disable=invalid-name
def test_bad_integer_set(constants):
    """Validate set operation over bad values"""
    constants.REQUIRED_INTEGER_TO_SET = 2
    assert constants.REQUIRED_INTEGER_TO_SET == 2


@parametrized_constants_source
# pylint: disable=invalid-name
def test_missing_integer_set(constants):
    """Validate set operation over missing values"""
    constants.REQUIRED_BUT_MISSING_INTEGER_TO_SET = 3
    assert constants.REQUIRED_BUT_MISSING_INTEGER_TO_SET == 3


@parametrized_constants_source
def test_defined_required_list(constants):
    """Check required defined list variable"""
    assert isinstance(constants.REQUIRED_DEFINED_LIST, list)
    assert constants.REQUIRED_DEFINED_LIST == ["REQUIRED_DEFINED_LIST defined value"]


@parametrized_constants_source
def test_defined_optional_list(constants):
    """Check optional defined list variable"""
    assert isinstance(constants.OPTIONAL_DEFINED_LIST, list)
    assert constants.OPTIONAL_DEFINED_LIST == ["OPTIONAL_DEFINED_LIST defined value"]


@parametrized_constants_source
def test_undefined_required_list(constants):
    """Check required undefined list variable"""
    with pytest.raises(MissingVariableError):
        assert constants.REQUIRED_UNDEFINED_LIST


@parametrized_constants_source
def test_undefined_optional_list(constants):
    """Check optional undefined list variable"""
    assert isinstance(constants.OPTIONAL_UNDEFINED_LIST, list)
    assert constants.OPTIONAL_UNDEFINED_LIST == ["OPTIONAL_UNDEFINED_LIST default value"]
