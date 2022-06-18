"""Class-based environment variables typed specification"""

from .namespace import (
    EnvironmentNamespace,
    MissingVariableError,
)
from .variables import (
    RequiredString,
    RequiredInteger,
    RequiredFloat,
    RequiredBoolean,
    OptionalString,
    OptionalInteger,
    OptionalFloat,
    OptionalBoolean,
)
from .version import __version__
