"""Base container class definition"""

import os
import typing as t

__all__ = [
    "EnvironmentNamespace",
]


class EnvironmentNamespace:
    """Optional namespace to provide common environment dictionary replacement"""

    environ: t.MutableMapping[str, str] = os.environ

    def __init__(self, *, environ: t.Optional[t.MutableMapping[str, str]] = None) -> None:
        if environ is not None:
            self.environ = environ
