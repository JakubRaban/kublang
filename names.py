from typing import Any


class NameTable:
    def __init__(self):
        self.variables = [{}]
        self.functions = [{}]

    def declare_variable(self, var_name: str, var_type: type):
        if self._get_scope_with_variable(var_name):
            raise ValueError(f"Variable '{var_name}' was already declared")
        self.variables[-1][var_name] = {'type': var_type, 'value': None}

    def assign_variable(self, var_name: str, value: Any):
        if not (scope := self._get_scope_with_variable(var_name)):
            raise KeyError(f"'{var_name}' was not declared")
        if isinstance(value, scope[var_name]['type']):
            scope[var_name]['value'] = value
        else:
            raise TypeError("Type mismatch between declared and assigned value")

    def get(self, var_name: str):
        for scope in reversed(self.variables):
            if var_name in scope:
                if self._is_assigned(var_name, scope):
                    return scope[var_name]['value']
                else:
                    raise ValueError(f"Variable '{var_name}' referenced before assignment")
        raise KeyError(f"Variable '{var_name}' was not declared")

    def declare_function(self):
        pass

    def add_scope(self):
        self.variables.append({})
        self.functions.append({})
        return self

    def remove_scope(self):
        self.variables.pop()
        self.functions.pop()
        return self

    def _get_scope_with_variable(self, var_name: str):
        for scope in reversed(self.variables):
            if var_name in scope:
                return scope
        return None

    def _is_assigned(self, name: str, scope: dict):
        return name in scope and scope[name]['value'] is not None
