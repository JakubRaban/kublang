
def to_python_type(lang_type):
    if lang_type == 'int':
        t = int
    elif lang_type == 'string':
        t = str
    elif lang_type == 'float':
        t = float
    elif lang_type == 'boolean':
        t = bool
    return t


def check_type_match(*values):
    if len(list(dict.fromkeys([type(val) for val in values]))) != 1:
        raise TypeError(f"Operands are not of the same type")
    return values[0]


def check_numeric_type(*values):
    types = [int, float]
    for value in values:
        if type(value) not in types:
            raise TypeError("All operands must be numeric for this operation")


def check_boolean_type(*values):
    for value in values:
        if type(value) != bool:
            raise TypeError("All operands must be boolean for this operation")


def check_string_type(*values):
    for value in values:
        if type(value) != str:
            raise TypeError("All operands must be string for this operation")


def check_int_type(*values):
    for value in values:
        if type(value) != int:
            raise TypeError("All operands must be string for this operation")