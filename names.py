from typing import Any, Optional


class NameTable:
    def __init__(self, initial_variables: Optional[dict] = None, initial_functions: Optional[dict] = None):
        self.variables = [{}] if initial_variables is None else [initial_variables]
        self.functions = initial_functions or {}

    def declare_variable(self, var_name: str, var_type: type, is_global: bool = False):
        if self._get_scope_with_variable(var_name):
            raise ValueError(f"Variable '{var_name}' was already declared")
        scope = 0 if is_global else -1
        self.variables[scope][var_name] = {'type': var_type, 'value': None}

    def assign_variable(self, var_name: str, value: Any):
        if not (scope := self._get_scope_with_variable(var_name)):
            raise KeyError(f"'{var_name}' was not declared")
        if isinstance(value, scope[var_name]['type']):
            scope[var_name]['value'] = value
        else:
            raise TypeError("Type mismatch between declared and assigned value")

    def get_variable(self, var_name: str):
        for scope in reversed(self.variables):
            if var_name in scope:
                if self._is_assigned(var_name, scope):
                    return scope[var_name]['value']
                else:
                    raise ValueError(f"Variable '{var_name}' referenced before assignment")
        raise KeyError(f"Variable '{var_name}' was not declared")

    def declare_function(self, fun_name, arguments, body, return_type):
        if fun_name in self.functions:
            raise ValueError(f"Function '{fun_name}' was already declared")
        self.functions[fun_name] = {
            'arguments': arguments,
            'body': body,
            'return_type': return_type,
        }

    def get_function(self, fun_name):
        if fun_name not in self.functions:
            raise ValueError(f"Function '{fun_name}' has not been declared")
        return self.functions[fun_name]

    def add_scope(self):
        self.variables.append({})
        return self

    def remove_scope(self):
        self.variables.pop()
        return self

    def _get_scope_with_variable(self, var_name: str):
        for scope in reversed(self.variables):
            if var_name in scope:
                return scope
        return None

    def _is_assigned(self, name: str, scope: dict):
        return name in scope and scope[name]['value'] is not None
