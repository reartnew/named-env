"""Base container class definition"""

import os
import typing as t

__all__ = [
    "EnvironmentNamespace",
]


class EnvironmentNamespace:
    """Optional namespace to provide common environment dictionary replacement"""

    def __init__(self, *, environ: t.Optional[t.MutableMapping[str, str]] = None) -> None:
        self.env: t.MutableMapping[str, str] = environ if environ is not None else os.environ
