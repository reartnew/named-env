"""Class-based environment variables typed specification"""

from .environment import (
    Environment,
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
