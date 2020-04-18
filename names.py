
class Variables:
    def __init__(self):
        self.names = {}

    def declare(self, name: str, var_type: type):
        if name in self.names:
            raise ValueError("Variable with this name was already declared")
        self.names[name] = {'type': var_type, 'value': None}

    def assign(self, name: str, value):
        if isinstance(value, self.names[name]['type']):
            self.names[name]['value'] = value
        else:
            raise TypeError("Type mismatch between declared and assigned value")

    def get(self, name: str):
        return self.names[name]['value']

class Functions:
    pass