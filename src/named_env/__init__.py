"""Class-based environment variables typed specification"""

from .exceptions import (
    MissingVariableError,
    ChoiceValueError,
)
from .namespace import EnvironmentNamespace
from .variables import (
    RequiredString,
    RequiredInteger,
    RequiredFloat,
    RequiredBoolean,
    RequiredTernary,
    RequiredList,
    RequiredPath,
    RequiredPathList,
    OptionalString,
    OptionalInteger,
    OptionalFloat,
    OptionalBoolean,
    OptionalTernary,
    OptionalList,
    OptionalPath,
    OptionalPathList,
)
from .version import __version__
