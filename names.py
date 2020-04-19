
class VariableArray:
    def __init__(self):
        self.names = {}

    def declare(self, name: str, var_type: type):
        if name in self.names:
            raise ValueError(f"Variable '{name}' was already declared")
        self.names[name] = {'type': var_type, 'value': None}

    def assign(self, name: str, value):
        if isinstance(value, self.names[name]['type']):
            self.names[name]['value'] = value
        else:
            raise TypeError("Type mismatch between declared and assigned value")

    def get(self, name: str):
        if not self._is_assigned(name):
            raise ValueError(f"Variable referenced before assignment: '{name}'")
        return self.names[name]['value']

    def _is_assigned(self, name: str):
        return name in self.names and self.names[name]['value'] is not None


class FunctionArray:
    pass