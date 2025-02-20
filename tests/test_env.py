"""EnvironmentNamespace tests"""

import pathlib
import typing as t

import pytest

from named_env import (
    EnvironmentNamespace,
    RequiredString,
    OptionalString,
    RequiredInteger,
    RequiredFloat,
    RequiredBoolean,
    RequiredTernary,
    RequiredList,
    OptionalList,
    OptionalBoolean,
    OptionalTernary,
    MissingVariableError,
    ChoiceValueError,
    RequiredPath,
    OptionalPath,
    RequiredPathList,
    OptionalPathList,
)

# Test environment dict
# pylint: disable=use-dict-literal
environ = dict(
    REQUIRED_DEFINED_STRING="REQUIRED_DEFINED_STRING defined value",
    OPTIONAL_DEFINED_STRING="OPTIONAL_DEFINED_STRING defined value",
    GOOD_INTEGER="1",
    GOOD_FLOAT="10.",
    GOOD_BOOLEAN="N",
    BAD_INTEGER="Foo",
    BAD_FLOAT="Bar",
    BAD_BOOLEAN="Baz",
    OPTIONAL_DEFINED_BOOLEAN="Y",
    EMPTY_DEFINED_BOOLEAN="",
    REQUIRED_STRING_TO_SET="REQUIRED_STRING_TO_SET value before set",
    REQUIRED_INTEGER_TO_SET="Not even an integer",
    REQUIRED_DEFINED_LIST="REQUIRED_DEFINED_LIST defined value",
    OPTIONAL_DEFINED_LIST="OPTIONAL_DEFINED_LIST defined value",
    CHOICE_CORRECTLY_DEFINED_REQUIRED_STRING="CHOICE_CORRECTLY_DEFINED_REQUIRED_STRING correct value",
    CHOICE_INCORRECTLY_DEFINED_REQUIRED_STRING="CHOICE_INCORRECTLY_DEFINED_REQUIRED_STRING incorrect value",
    CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST=(
        "CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST correct value,CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST correct value"
    ),
    CHOICE_INCORRECTLY_DEFINED_REQUIRED_LIST=(
        "CHOICE_INCORRECTLY_DEFINED_REQUIRED_LIST correct value,"
        "CHOICE_INCORRECTLY_DEFINED_REQUIRED_LIST incorrect value"
    ),
    REQUIRED_TERNARY_TRUE="Y",
    REQUIRED_TERNARY_FALSE="N",
    REQUIRED_TERNARY_NONE="None",
    REQUIRED_TERNARY_EMPTY="",
    REQUIRED_DEFINED_PATH="/",
    OPTIONAL_DEFINED_PATH=".",
    REQUIRED_DEFINED_PATH_LIST="/foo:/bar",
    OPTIONAL_DEFINED_PATH_LIST="/foo:/bar",
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
    OPTIONAL_DEFINED_BOOLEAN = OptionalBoolean(False)
    OPTIONAL_UNDEFINED_BOOLEAN = OptionalBoolean(True)
    EMPTY_DEFINED_BOOLEAN = RequiredBoolean()
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
    CHOICE_CORRECTLY_DEFINED_REQUIRED_STRING = RequiredString(
        choice=["CHOICE_CORRECTLY_DEFINED_REQUIRED_STRING correct value"]
    )
    CHOICE_INCORRECTLY_DEFINED_REQUIRED_STRING = RequiredString(
        choice=["CHOICE_INCORRECTLY_DEFINED_REQUIRED_STRING correct value"]
    )
    CHOICE_CORRECTLY_DEFINED_OPTIONAL_STRING = OptionalString(
        "CHOICE_CORRECTLY_DEFINED_OPTIONAL_STRING correct value",
        choice=["CHOICE_CORRECTLY_DEFINED_OPTIONAL_STRING correct value"],
    )
    CHOICE_INCORRECTLY_DEFINED_OPTIONAL_STRING = OptionalString(
        "CHOICE_INCORRECTLY_DEFINED_OPTIONAL_STRING incorrect value",
        choice=["CHOICE_INCORRECTLY_DEFINED_OPTIONAL_STRING correct value"],
    )
    CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST = RequiredList(
        choice=["CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST correct value"]
    )
    CHOICE_INCORRECTLY_DEFINED_REQUIRED_LIST = RequiredList(
        choice=["CHOICE_INCORRECTLY_DEFINED_REQUIRED_LIST correct value"]
    )
    CACHE_TEST_STRING = RequiredString()
    REQUIRED_TERNARY_TRUE = RequiredTernary()
    REQUIRED_TERNARY_FALSE = RequiredTernary()
    REQUIRED_TERNARY_NONE = RequiredTernary()
    REQUIRED_TERNARY_EMPTY = RequiredTernary()
    OPTIONAL_TERNARY_OBJECT_TRUE = OptionalTernary(True)
    OPTIONAL_TERNARY_OBJECT_FALSE = OptionalTernary(False)
    OPTIONAL_TERNARY_OBJECT_NONE = OptionalTernary(None)
    OPTIONAL_TERNARY_STRING_TRUE = OptionalTernary("true")
    OPTIONAL_TERNARY_STRING_FALSE = OptionalTernary("false")
    OPTIONAL_TERNARY_STRING_NONE = OptionalTernary("none")
    REQUIRED_DEFINED_PATH = RequiredPath()
    REQUIRED_UNDEFINED_PATH = RequiredPath()
    OPTIONAL_DEFINED_PATH = OptionalPath("/")
    OPTIONAL_UNDEFINED_PATH = OptionalPath("/")
    REQUIRED_DEFINED_PATH_LIST = RequiredPathList()
    REQUIRED_UNDEFINED_PATH_LIST = RequiredPathList()
    OPTIONAL_DEFINED_PATH_LIST = OptionalPathList("/baz:/qux")
    OPTIONAL_UNDEFINED_PATH_LIST = OptionalPathList("/baz:/qux")


def parametrized_constants_source(func):
    """Check both type-based and instance-based definitions"""

    class ConstantsClass(PytestEnvironmentNamespace):
        """Used for class-based (not instance-based) access tests"""

        environ = environ

    return pytest.mark.parametrize(
        argnames="constants",
        argvalues=[PytestEnvironmentNamespace(environ=environ), ConstantsClass],
        ids=["instance", "type"],
    )(func)


ConstantsType = t.Union[PytestEnvironmentNamespace, type[PytestEnvironmentNamespace]]


@parametrized_constants_source
def test_defined_required_string(constants: ConstantsType) -> None:
    """Check required defined string variable"""
    assert isinstance(constants.REQUIRED_DEFINED_STRING, str)
    assert constants.REQUIRED_DEFINED_STRING == "REQUIRED_DEFINED_STRING defined value"


@parametrized_constants_source
def test_defined_optional_string(constants: ConstantsType) -> None:
    """Check optional defined string variable"""
    assert isinstance(constants.OPTIONAL_DEFINED_STRING, str)
    assert constants.OPTIONAL_DEFINED_STRING == "OPTIONAL_DEFINED_STRING defined value"


@parametrized_constants_source
def test_undefined_required_string(constants: ConstantsType) -> None:
    """Check required undefined string variable"""
    with pytest.raises(MissingVariableError):
        assert constants.REQUIRED_UNDEFINED_STRING


@parametrized_constants_source
def test_undefined_optional_string(constants: ConstantsType) -> None:
    """Check optional undefined string variable"""
    assert isinstance(constants.OPTIONAL_UNDEFINED_STRING, str)
    assert constants.OPTIONAL_UNDEFINED_STRING == "OPTIONAL_UNDEFINED_STRING default value"


@parametrized_constants_source
def test_good_int(constants: ConstantsType) -> None:
    """Check integer cast"""
    assert isinstance(constants.GOOD_INTEGER, int)
    assert constants.GOOD_INTEGER == 1


@parametrized_constants_source
def test_good_float(constants: ConstantsType) -> None:
    """Check float cast"""
    assert isinstance(constants.GOOD_FLOAT, float)
    assert constants.GOOD_FLOAT == 10.0


@parametrized_constants_source
def test_good_bool(constants: ConstantsType) -> None:
    """Check boolean cast"""
    assert isinstance(constants.GOOD_BOOLEAN, bool)
    assert not constants.GOOD_BOOLEAN


@parametrized_constants_source
def test_bad_int(constants: ConstantsType) -> None:
    """Check integer cast failure"""
    with pytest.raises(ValueError, match="invalid literal for int"):
        assert constants.BAD_INTEGER


@parametrized_constants_source
def test_bad_float(constants: ConstantsType) -> None:
    """Check float cast failure"""
    with pytest.raises(ValueError, match="could not convert string to float"):
        assert constants.BAD_FLOAT


@parametrized_constants_source
def test_bad_bool(constants: ConstantsType) -> None:
    """Check boolean cast failure"""
    with pytest.raises(ChoiceValueError):
        assert constants.BAD_BOOLEAN is False


@parametrized_constants_source
# pylint: disable=invalid-name
def test_required_string_set(constants: ConstantsType) -> None:
    """Check set operation on required strings"""
    assert constants.REQUIRED_STRING_TO_SET == "REQUIRED_STRING_TO_SET value before set"
    constants.REQUIRED_STRING_TO_SET = "REQUIRED_STRING_TO_SET value after set"
    assert constants.REQUIRED_STRING_TO_SET == "REQUIRED_STRING_TO_SET value after set"


@parametrized_constants_source
# pylint: disable=invalid-name
def test_optional_string_set(constants: ConstantsType) -> None:
    """Check set operation on optional strings"""
    assert constants.OPTIONAL_STRING_TO_SET == "OPTIONAL_STRING_TO_SET value before set"
    constants.OPTIONAL_STRING_TO_SET = "OPTIONAL_STRING_TO_SET value after set"
    assert constants.OPTIONAL_STRING_TO_SET == "OPTIONAL_STRING_TO_SET value after set"


@parametrized_constants_source
# pylint: disable=invalid-name
def test_bad_integer_set(constants: ConstantsType) -> None:
    """Validate set operation over bad values"""
    constants.REQUIRED_INTEGER_TO_SET = 2
    assert constants.REQUIRED_INTEGER_TO_SET == 2


@parametrized_constants_source
# pylint: disable=invalid-name
def test_missing_integer_set(constants: ConstantsType) -> None:
    """Validate set operation over missing values"""
    constants.REQUIRED_BUT_MISSING_INTEGER_TO_SET = 3
    assert constants.REQUIRED_BUT_MISSING_INTEGER_TO_SET == 3


@parametrized_constants_source
def test_defined_required_list(constants: ConstantsType) -> None:
    """Check required defined list variable"""
    assert isinstance(constants.REQUIRED_DEFINED_LIST, list)
    assert constants.REQUIRED_DEFINED_LIST == ["REQUIRED_DEFINED_LIST defined value"]


@parametrized_constants_source
def test_defined_optional_list(constants: ConstantsType) -> None:
    """Check optional defined list variable"""
    assert isinstance(constants.OPTIONAL_DEFINED_LIST, list)
    assert constants.OPTIONAL_DEFINED_LIST == ["OPTIONAL_DEFINED_LIST defined value"]


@parametrized_constants_source
def test_undefined_required_list(constants: ConstantsType) -> None:
    """Check required undefined list variable"""
    with pytest.raises(MissingVariableError):
        assert constants.REQUIRED_UNDEFINED_LIST


@parametrized_constants_source
def test_undefined_optional_list(constants: ConstantsType) -> None:
    """Check optional undefined list variable"""
    assert isinstance(constants.OPTIONAL_UNDEFINED_LIST, list)
    assert constants.OPTIONAL_UNDEFINED_LIST == ["OPTIONAL_UNDEFINED_LIST default value"]


@parametrized_constants_source
def test_choice_required_string_correct(constants: ConstantsType) -> None:
    """Check choice-based correct required string variable"""
    assert isinstance(constants.CHOICE_CORRECTLY_DEFINED_REQUIRED_STRING, str)
    assert (
        constants.CHOICE_CORRECTLY_DEFINED_REQUIRED_STRING == "CHOICE_CORRECTLY_DEFINED_REQUIRED_STRING correct value"
    )


@parametrized_constants_source
def test_choice_required_string_incorrect(constants: ConstantsType) -> None:
    """Check choice-based incorrect required string variable"""
    with pytest.raises(ChoiceValueError, match="unexpected value"):
        assert isinstance(constants.CHOICE_INCORRECTLY_DEFINED_REQUIRED_STRING, str)


@parametrized_constants_source
def test_choice_optional_string_correct(constants: ConstantsType) -> None:
    """Check choice-based correct optional string variable"""
    assert isinstance(constants.CHOICE_CORRECTLY_DEFINED_OPTIONAL_STRING, str)
    assert (
        constants.CHOICE_CORRECTLY_DEFINED_OPTIONAL_STRING == "CHOICE_CORRECTLY_DEFINED_OPTIONAL_STRING correct value"
    )


@parametrized_constants_source
def test_choice_optional_string_incorrect(constants: ConstantsType) -> None:
    """Check choice-based incorrect optional string variable"""
    with pytest.raises(ChoiceValueError, match="unexpected value"):
        assert isinstance(constants.CHOICE_INCORRECTLY_DEFINED_OPTIONAL_STRING, str)


@parametrized_constants_source
def test_choice_list_correct(constants: ConstantsType) -> None:
    """Check choice-based correct list variable"""
    assert isinstance(constants.CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST, list)
    assert constants.CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST == [
        "CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST correct value",
        "CHOICE_CORRECTLY_DEFINED_REQUIRED_LIST correct value",
    ]


def test_invalid_choice_value() -> None:
    """Check incorrect choice value"""
    with pytest.raises(ValueError, match="'choice' argument must be a sequence"):
        RequiredString(choice={})  # type: ignore


@parametrized_constants_source
def test_enabled_cache(constants: ConstantsType) -> None:
    """Check enabled cache"""
    constants.environ["CACHE_TEST_STRING"] = "Foo"
    assert constants.CACHE_TEST_STRING == "Foo"
    constants.environ["CACHE_TEST_STRING"] = "Bar"
    assert constants.CACHE_TEST_STRING == "Foo"


@parametrized_constants_source
def test_disabled_cache(constants: ConstantsType) -> None:
    """Check disabled cache"""
    constants.cache_values = False
    constants.environ["CACHE_TEST_STRING"] = "Foo"
    assert constants.CACHE_TEST_STRING == "Foo"
    constants.environ["CACHE_TEST_STRING"] = "Bar"
    assert constants.CACHE_TEST_STRING == "Bar"


@parametrized_constants_source
def test_optional_boolean(constants: ConstantsType) -> None:
    """Check optional boolean"""
    assert constants.OPTIONAL_DEFINED_BOOLEAN is True
    assert constants.OPTIONAL_UNDEFINED_BOOLEAN is True


@parametrized_constants_source
def test_empty_boolean(constants: ConstantsType) -> None:
    """Check empty-string boolean"""
    assert constants.EMPTY_DEFINED_BOOLEAN is False


@parametrized_constants_source
def test_required_ternary(constants: ConstantsType) -> None:
    """Check required ternary values"""
    assert constants.REQUIRED_TERNARY_TRUE is True
    assert constants.REQUIRED_TERNARY_FALSE is False
    assert constants.REQUIRED_TERNARY_NONE is None
    assert constants.REQUIRED_TERNARY_EMPTY is None


@parametrized_constants_source
def test_optional_ternary(constants: ConstantsType) -> None:
    """Check optional ternary values"""
    assert constants.OPTIONAL_TERNARY_STRING_TRUE is True
    assert constants.OPTIONAL_TERNARY_STRING_FALSE is False
    assert constants.OPTIONAL_TERNARY_STRING_NONE is None
    assert constants.OPTIONAL_TERNARY_OBJECT_TRUE is True
    assert constants.OPTIONAL_TERNARY_OBJECT_FALSE is False
    assert constants.OPTIONAL_TERNARY_OBJECT_NONE is None


@parametrized_constants_source
def test_required_path(constants: ConstantsType) -> None:
    """Check required path"""
    assert isinstance(constants.REQUIRED_DEFINED_PATH, pathlib.Path)


@parametrized_constants_source
def test_undefined_required_path(constants: ConstantsType) -> None:
    """Check required undefined path"""
    with pytest.raises(MissingVariableError):
        assert constants.REQUIRED_UNDEFINED_PATH


@parametrized_constants_source
def test_optional_path(constants: ConstantsType) -> None:
    """Check optional path"""
    assert constants.OPTIONAL_DEFINED_PATH == pathlib.Path(".")


@parametrized_constants_source
def test_undefined_optional_path(constants: ConstantsType) -> None:
    """Check optional undefined path"""
    assert constants.OPTIONAL_UNDEFINED_PATH == pathlib.Path("/")


@parametrized_constants_source
def test_required_path_list(constants: ConstantsType) -> None:
    """Check required path list"""
    assert isinstance(constants.REQUIRED_DEFINED_PATH_LIST, list)
    assert all(isinstance(item, pathlib.Path) for item in constants.REQUIRED_DEFINED_PATH_LIST)


@parametrized_constants_source
def test_undefined_required_path_list(constants: ConstantsType) -> None:
    """Check required undefined path list"""
    with pytest.raises(MissingVariableError):
        assert constants.REQUIRED_UNDEFINED_PATH_LIST


@parametrized_constants_source
def test_optional_path_list(constants: ConstantsType) -> None:
    """Check optional path list"""
    assert constants.OPTIONAL_DEFINED_PATH_LIST == [pathlib.Path("/foo"), pathlib.Path("/bar")]


@parametrized_constants_source
def test_undefined_optional_path_list(constants: ConstantsType) -> None:
    """Check optional undefined path list"""
    assert constants.OPTIONAL_UNDEFINED_PATH_LIST == [pathlib.Path("/baz"), pathlib.Path("/qux")]
