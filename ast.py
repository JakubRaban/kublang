
import abc
from typing import List, Union
import names

import helpers


class Node(abc.ABC):
    def __str__(self, level=0):
        ret = '\t' * level + self.get_symbol() + '\n'
        for child in self.get_children():
            ret += child.__str__(level + 1)
        return ret

    @abc.abstractmethod
    def evaluate(self, name_table):
        pass

    @abc.abstractmethod
    def get_symbol(self) -> str:
        return self.__class__.__name__

    @abc.abstractmethod
    def get_children(self) -> List:
        pass

    @property
    @abc.abstractmethod
    def is_constant(self) -> bool:
        pass


class Program(Node):
    def __init__(self, program):
        self.program = program

    def evaluate(self, name_table):
        self.program.evaluate(name_table)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.program]

    @property
    def is_constant(self) -> bool:
        return self.program.is_constant


class Lines(Node):
    def __init__(self, lines: List[Node]):
        self.lines = lines

    def evaluate(self, name_table):
        for line in self.lines:
            result = line.evaluate(name_table)
            if isinstance(line, ReturnStatement):
                return result

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List[Node]:
        return self.lines

    @property
    def is_constant(self) -> bool:
        return all([line.is_constant for line in self.lines])


class Number(Node):
    def __init__(self, value: Union[int, float]):
        self.value = value

    def evaluate(self, name_table):
        return self.value

    def get_symbol(self) -> str:
        return f"{super().get_symbol()}({self.value})"

    def get_children(self) -> List[str]:
        return []

    @property
    def is_constant(self) -> bool:
        return True


class BinaryMathOperator(Node):
    def __init__(self, operation: str, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluate(self, name_table):
        l, r = self.left.evaluate(name_table), self.right.evaluate(name_table)
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
            res = l / r
            if res - int(res) == 0:
                res = int(res)
            return res
        elif self.operation == '^':
            return l ** r
        elif self.operation == '%':
            return l % r

    def get_children(self) -> List[Node]:
        return [self.left, self.right]

    def get_symbol(self) -> str:
        return f"{super().get_symbol()}({self.operation})"

    @property
    def is_constant(self) -> bool:
        return self.left.is_constant and self.right.is_constant


class UnaryMathOperator(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def evaluate(self, name_table):
        o = self.operand.evaluate(name_table)
        helpers.check_numeric_type(o)
        if self.operator == '-':
            return -o

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.operator})'

    def get_children(self) -> List:
        return [self.operand]

    @property
    def is_constant(self) -> bool:
        return self.operand.is_constant


class BinaryLogicalOperator(Node):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluate(self, name_table):
        l, r = self.left.evaluate(name_table), self.right.evaluate(name_table)
        helpers.check_boolean_type(l, r)
        if self.operation == '&&':
            return l and r
        elif self.operation == '||':
            return l or r

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.operation})'

    def get_children(self) -> List:
        return [self.left, self.right]

    @property
    def is_constant(self) -> bool:
        return self.left.is_constant and self.right.is_constant


class UnaryLogicalOperator(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def evaluate(self, name_table):
        o = self.operand.evaluate(name_table)
        helpers.check_boolean_type(o)
        if self.operator == '!':
            return not o

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.operator})'

    def get_children(self) -> List:
        return [self.operand]

    @property
    def is_constant(self) -> bool:
        return self.operand.is_constant


class Comparison(Node):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluate(self, name_table):
        l, r = self.left.evaluate(name_table), self.right.evaluate(name_table)
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

    @property
    def is_constant(self) -> bool:
        return self.left.is_constant and self.right.is_constant


class Declaration(Node):
    def __init__(self, type_name, var_name, is_global=False):
        self.type_name = type_name
        self.var_name = var_name
        self.is_global = is_global

    def evaluate(self, name_table):
        type_name = self.type_name.evaluate(name_table)
        if type_name == 'void':
            raise ValueError("Variables cannot be of type void")
        our_type = helpers.to_python_type(type_name)
        name_table.declare_variable(self.var_name.evaluate(name_table), our_type, self.is_global)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.type_name, self.var_name]

    @property
    def is_constant(self) -> bool:
        return False


class Assignment(Node):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def evaluate(self, name_table):
        l, r = self.var_name.evaluate(name_table), self.value.evaluate(name_table)
        name_table.assign_variable(l, r)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.var_name, self.value]

    @property
    def is_constant(self) -> bool:
        return False


class DeclarationWithAssignment(Node):
    def __init__(self, type_name, var_name, value, is_global):
        self.type_name = type_name
        self.var_name = var_name
        self.value = value
        self.is_global = is_global

    def evaluate(self, name_table):
        Declaration(self.type_name, self.var_name, self.is_global).evaluate(name_table)
        Assignment(self.var_name, self.value).evaluate(name_table)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.type_name, self.var_name, self.value]

    @property
    def is_constant(self) -> bool:
        return False


class FunctionDeclaration(Node):
    def __init__(self, function_name, arguments, body, return_type):
        self.function_name = function_name
        self.arguments = arguments
        self.body = body
        self.return_type = return_type

    def evaluate(self, name_table):
        arguments = [(helpers.to_python_type(argument[0]), argument[1])
                     for argument in self.arguments.evaluate(name_table)]
        name_table.declare_function(
            fun_name=self.function_name.evaluate(name_table),
            arguments=arguments,
            body=self.body,
            return_type=helpers.to_python_type(self.return_type.evaluate(name_table)),
        )

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.return_type, self.function_name, self.arguments, self.body]

    @property
    def is_constant(self) -> bool:
        return False


class FunctionArguments(Node):
    def __init__(self, arguments):
        self.arguments = arguments

    def evaluate(self, name_table):
        return [argument.evaluate(name_table) for argument in self.arguments]

    def get_symbol(self) -> str:
        return f"{super().get_symbol()}{'(empty)' if not self.arguments else ''}"

    def get_children(self) -> List:
        return self.arguments

    @property
    def is_constant(self) -> bool:
        return True


class FunctionArgument(Node):
    def __init__(self, type_name, arg_name):
        self.type_name = type_name
        self.arg_name = arg_name

    def evaluate(self, name_table):
        return self.type_name.evaluate(name_table), self.arg_name.evaluate(name_table)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.type_name, self.arg_name]

    @property
    def is_constant(self) -> bool:
        return True


class ReturnStatement(Node):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, name_table):
        return self.expression.evaluate(name_table)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.expression]

    @property
    def is_constant(self) -> bool:
        return self.expression.is_constant


class FunctionCall(Node):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def evaluate(self, name_table):
        function_spec = name_table.get_function(self.name.evaluate(name_table))
        call_spec = self.arguments.evaluate(name_table)
        if (required := len(function_spec['arguments'])) != (provided := len(call_spec)):
            raise ValueError(f"Function '{self.name}' requires {required} arguments but got {provided}")
        function_variables = {}
        for index, matched_arg in enumerate(zip(function_spec['arguments'], call_spec)):
            if (expected_type := matched_arg[0][0]) != (actual_type := matched_arg[1][0]):
                raise TypeError(f"Type mismatch in argument number {index}: expected {expected_type}, got {actual_type}")
            function_variables[matched_arg[0][1]] = {'type': actual_type, 'value': matched_arg[1][1]}
        function_name_table = names.NameTable(function_variables, name_table.functions)
        function_return = function_spec['body'].evaluate(function_name_table)
        if not isinstance(function_return, function_spec['return_type']):
            raise TypeError(f"Value returned from function is of type {type(function_return)} but expected {function_spec['return_type']}")
        return function_return

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.name, self.arguments]

    @property
    def is_constant(self) -> bool:
        return False


class FunctionCallArguments(Node):
    def __init__(self, arguments):
        self.arguments = arguments

    def evaluate(self, name_table):
        return [(type(argument), argument) for argument in [arg.evaluate(name_table) for arg in self.arguments]]

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return self.arguments

    @property
    def is_constant(self) -> bool:
        return all([arg.is_constant for arg in self.arguments])


class VariableName(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, name_table):
        return self.name

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.name})'

    def get_children(self) -> List:
        return []

    @property
    def is_constant(self) -> bool:
        return True


class TypeName(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, name_table):
        return self.name

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.name})'

    def get_children(self) -> List:
        return []

    @property
    def is_constant(self) -> bool:
        return True


class VariableRead(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, name_table):
        return name_table.get_variable(self.name)

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.name})'

    def get_children(self) -> List:
        return []

    @property
    def is_constant(self) -> bool:
        return False


class String(Node):
    def __init__(self, text):
        self.text = text

    def evaluate(self, name_table):
        return self.text

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.text})'

    def get_children(self) -> List:
        return []

    @property
    def is_constant(self) -> bool:
        return True


class TrueOrFalse(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, name_table):
        return self.value

    def get_symbol(self) -> str:
        return f'{super().get_symbol()}({self.value})'

    def get_children(self) -> List:
        return []

    @property
    def is_constant(self) -> bool:
        return True


class IfStatement(Node):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def evaluate(self, name_table):
        condition = self.condition.evaluate(name_table)
        helpers.check_boolean_type(condition)
        if condition:
            self.statement.evaluate(name_table.add_scope())
        name_table.remove_scope()

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.condition, self.statement]

    @property
    def is_constant(self) -> bool:
        return False


class IfElseStatement(Node):
    def __init__(self, condition, on_true_statement, on_false_statement):
        self.condition = condition
        self.on_true_statement = on_true_statement
        self.on_false_statement = on_false_statement

    def evaluate(self, name_table):
        condition = self.condition.evaluate(name_table)
        helpers.check_boolean_type(condition)
        name_table.add_scope()
        if condition:
            self.on_true_statement.evaluate(name_table)
        else:
            self.on_false_statement.evaluate(name_table)
        name_table.remove_scope()

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.condition, self.on_true_statement, self.on_false_statement]

    @property
    def is_constant(self) -> bool:
        return False


class WhileStatement(Node):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def evaluate(self, name_table):
        condition = self.condition.evaluate(name_table)
        helpers.check_boolean_type(condition)
        while condition:
            self.statement.evaluate(name_table.add_scope())
            name_table.remove_scope()
            condition = self.condition.evaluate(name_table)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.condition, self.statement]

    @property
    def is_constant(self) -> bool:
        return False


class Print(Node):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, name_table):
        print(self.expression.evaluate(name_table))

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.expression]

    def is_constant(self) -> bool:
        return self.expression.is_constant


class IntToFloat(Node):
    def __init__(self, number):
        self.number = number

    def evaluate(self, name_table):
        number = self.number.evaluate(name_table)
        helpers.check_int_type(number)
        return float(number)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.number]

    @property
    def is_constant(self) -> bool:
        return self.number.is_constant


class FloatToInt(Node):
    def __init__(self, number):
        self.number = number

    def evaluate(self, name_table):
        number = self.number.evaluate(name_table)
        helpers.check_float_type(number)
        return int(number)

    def get_symbol(self) -> str:
        return super().get_symbol()

    def get_children(self) -> List:
        return [self.number]

    @property
    def is_constant(self) -> bool:
        return self.number.is_constant
