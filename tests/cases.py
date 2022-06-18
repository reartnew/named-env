"""Test cases"""

from typing import TypedDict, Optional

from pytest_data_suites import DataSuite

__all__ = [
    "OptionalStringToBooleanDataSuite",
]


class OptionalStringToBooleanCase(TypedDict):
    """An attempt to transform strings into booleans"""

    raw: Optional[str]
    result: bool


class OptionalStringToBooleanDataSuite(DataSuite):
    """Check regular acceptable boolean representations"""

    positive_y = OptionalStringToBooleanCase(raw="Y", result=True)
    positive_yes = OptionalStringToBooleanCase(raw="yes", result=True)
    positive_true = OptionalStringToBooleanCase(raw="True", result=True)
    positive_1 = OptionalStringToBooleanCase(raw="1", result=True)
    negative_n = OptionalStringToBooleanCase(raw="N", result=False)
    negative_no = OptionalStringToBooleanCase(raw="no", result=False)
    negative_false = OptionalStringToBooleanCase(raw="False", result=False)
    negative_0 = OptionalStringToBooleanCase(raw="0", result=False)
    negative_none = OptionalStringToBooleanCase(raw=None, result=False)
