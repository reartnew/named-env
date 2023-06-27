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
    OptionalString,
    OptionalInteger,
    OptionalFloat,
    OptionalBoolean,
    RequiredList,
    OptionalList,
)
from .version import __version__
