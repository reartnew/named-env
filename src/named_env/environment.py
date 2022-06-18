"""Base container class definition"""

import os
import textwrap
import typing as t

from . import variables

__all__ = [
    "Environment",
    "MissingVariableError",
]


class MissingVariableError(EnvironmentError):
    """Detailed error class for missing variables with description"""

    def __init__(self, variable: str, description: t.Optional[str]) -> None:
        message: str = variable
        if description is not None:
            message = f"{message}\n\n{textwrap.indent(description, ' ' * 8)}"
        super().__init__(message)
        self.variable = variable
        self.description = description


class Environment:
    """Lazy environment evaluation on first attribute get/set.
    Overrides __getattribute__ method, thus one should be much attentive while overriding methods."""

    def __init__(self) -> None:
        super().__init__()
        # `_resolved` property is an optional dictionary cache of all extracted variables
        super().__setattr__("_resolved", {})
        class_object = super().__getattribute__("__class__")
        # `_vars` property maps class `_Variable` attributes names to instances
        _vars: t.Dict[str, variables.BaseVariableMixin] = {}
        for k in dir(class_object):
            prop_value = getattr(class_object, k, None)
            if isinstance(prop_value, variables.BaseVariableMixin):
                _vars[k] = prop_value
        super().__setattr__("_vars", _vars)

    def __getattribute__(self, name: str) -> t.Any:
        # Default logic for non-`Variable` attributes
        attr = super().__getattribute__(name)
        vars_map: t.Dict[str, variables.BaseVariableMixin] = super().__getattribute__("_vars")
        if name not in vars_map:
            return attr
        cache = super().__getattribute__("_resolved")
        # Check cache
        if name in cache:
            return cache[name]
        env_var_object: variables.BaseVariableMixin = vars_map[name]
        if name in os.environ:
            cache[name] = env_var_object.cast(os.environ[name])
        elif isinstance(env_var_object, variables.OptionalVariableMixin):
            # Cast defaults also
            cache[name] = env_var_object.cast(env_var_object.default)
        elif isinstance(env_var_object, variables.RequiredVariableMixin):
            raise MissingVariableError(variable=name, description=attr.description)
        return cache[name]

    def __setattr__(self, key, value) -> None:
        # Non-`Variable` attributes
        if key not in super().__getattribute__("_vars"):
            return super().__setattr__(key, value)
        super().__getattribute__("_resolved")[key] = value
        return None
