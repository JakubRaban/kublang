
import abc
from typing import List, Union

import helpers


class Node(abc.ABC):
    def __str__(self, level=0):
        ret = '\t' * level + self.get_symbol() + '\n'
        for child in self.get_children():
            ret += child.__str__(level + 1)
        return ret

    @abc.abstractmethod
    def evaluate(self, variable_array):
        pass

    @abc.abstractmethod
    def get_symbol(self) -> str:
        return self.__class__.__name__

    @abc.abstractmethod
    def get_children(self) -> List:
        pass


class Program(Node):
    def __init__(self, program):
        self.program = program

    def evaluate(self, variable_array):
        self.program.evaluate(variable_array)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.program]


class Lines(Node):
    def __init__(self, lines: List[Node]):
        self.lines = lines

    def evaluate(self, variable_array):
        for line in self.lines:
            line.evaluate(variable_array)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List[Node]:
        return self.lines


class Number(Node):
    def __init__(self, value: Union[int, float]):
        self.value = value

    def evaluate(self, variable_array):
        return self.value

    def get_symbol(self) -> str:
        return f"{super().get_symbol()}({self.value})"

    def get_children(self) -> List[str]:
        return []


class BinaryMathOperator(Node):
    def __init__(self, operation: str, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluate(self, variable_array):
        l, r = self.left.evaluate(variable_array), self.right.evaluate(variable_array)
        helpers.check_type_match(l, r)
        helpers.check_numeric_or_string_type(l, r)
        if self.operation == '+':
            return l + r
        helpers.check_numeric_type(l, r)
        if self.operation == '-':
            return l - r
        elif self.operation == '*':
            return l * r
        elif self.operation == '/':
            return l / r
        elif self.operation == '^':
            return l ** r
        elif self.operation == '%':
            return l % r

    def get_children(self) -> List[Node]:
        return [self.left, self.right]

    def get_symbol(self) -> str:
        return f"{super().get_symbol()}({self.operation})"


class BinaryLogicalOperator(Node):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluate(self, variable_array):
        l, r = self.left.evaluate(variable_array), self.right.evaluate(variable_array)
        helpers.check_boolean_type(l, r)
        if self.operation == '&&':
            return l and r
        elif self.operation == '||':
            return l or r

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.operation})'

    def get_children(self) -> List:
        return [self.left, self.right]


class UnaryLogicalOperator(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def evaluate(self, variable_array):
        o = self.operand.evaluate(variable_array)
        helpers.check_boolean_type(o)
        if self.operator == '!':
            return not o

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.operator})'

    def get_children(self) -> List:
        return [self.operand]


class Comparison(Node):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluate(self, variable_array):
        l, r = self.left.evaluate(variable_array), self.right.evaluate(variable_array)
        helpers.check_type_match(l, r)
        helpers.check_numeric_type(l, r)
        if self.operation == '=':
            return l == r
        elif self.operation == '≠':
            return l != r
        elif self.operation == '>':
            return l > r
        elif self.operation == '>=':
            return l >= r
        elif self.operation == '<':
            return l < r
        elif self.operation == '<=':
            return l <= r

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.operation})'

    def get_children(self) -> List:
        return [self.left, self.right]


class Declaration(Node):
    def __init__(self, type_name, var_name):
        self.type_name = type_name
        self.var_name = var_name

    def evaluate(self, variable_array):
        our_type = helpers.to_python_type(self.type_name.evaluate(variable_array))
        variable_array.declare(self.var_name.evaluate(variable_array), our_type)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.type_name, self.var_name]


class Assignment(Node):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def evaluate(self, variable_array):
        l, r = self.var_name.evaluate(variable_array), self.value.evaluate(variable_array)
        variable_array.assign(l, r)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.var_name, self.value]


class DeclarationWithAssignment(Node):
    def __init__(self, type_name, var_name, value):
        self.type_name = type_name
        self.var_name = var_name
        self.value = value

    def evaluate(self, variable_array):
        Declaration(self.type_name, self.var_name).evaluate(variable_array)
        Assignment(self.var_name, self.value).evaluate(variable_array)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.type_name, self.var_name, self.value]


class VariableName(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, variable_array):
        return self.name

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.name})'

    def get_children(self) -> List:
        return []


class TypeName(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, variable_array):
        return self.name

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.name})'

    def get_children(self) -> List:
        return []


class VariableRead(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, variable_array):
        return variable_array.get(self.name)

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.name})'

    def get_children(self) -> List:
        return []


class String(Node):
    def __init__(self, text):
        self.text = text

    def evaluate(self, variable_array):
        return self.text

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.text})'

    def get_children(self) -> List:
        return []


class TrueOrFalse(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, variable_array):
        return self.value

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.value})'

    def get_children(self) -> List:
        return []


class IfStatement(Node):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def evaluate(self, variable_array):
        condition = self.condition.evaluate(variable_array)
        helpers.check_boolean_type(condition)
        if condition:
            self.statement.evaluate(variable_array)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.condition, self.statement]


class IfElseStatement(Node):
    def __init__(self, condition, on_true_statement, on_false_statement):
        self.condition = condition
        self.on_true_statement = on_true_statement
        self.on_false_statement = on_false_statement

    def evaluate(self, variable_array):
        condition = self.condition.evaluate(variable_array)
        helpers.check_boolean_type(condition)
        if condition:
            self.on_true_statement.evaluate(variable_array)
        else:
            self.on_false_statement.evaluate(variable_array)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.condition, self.on_true_statement, self.on_false_statement]


class WhileStatement(Node):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def evaluate(self, variable_array):
        condition = self.condition.evaluate(variable_array)
        helpers.check_boolean_type(condition)
        while condition:
            self.statement.evaluate(variable_array)
            condition = self.condition.evaluate(variable_array)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.condition, self.statement]


class Print(Node):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, variable_array):
        print(self.expression.evaluate(variable_array))

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.expression]


class IntToFloat(Node):
    def __init__(self, number):
        self.number = number

    def evaluate(self, variable_array):
        number = self.number.evaluate(variable_array)
        helpers.check_int_type(number)
        return float(number)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.number]


class FloatToInt(Node):
    def __init__(self, number):
        self.number = number

    def evaluate(self, variable_array):
        number = self.number.evaluate(variable_array)
        helpers.check_float_type(number)
        return int(number)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.number]
