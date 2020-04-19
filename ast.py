
from typing import Optional, List, Union

import helpers


class Node:
    pass


class Number(Node):
    def __init__(self, value: Union[int, float]):
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self):
        return self.value


class BinaryOperator(Node):
    def __init__(self, operation: str, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluate(self):
        l, r = self.left.evaluate(), self.right.evaluate()
        helpers.check_type_match(l, r)
        helpers.check_numeric_type(l, r)
        if self.operation == '+':
            return l + r
        elif self.operation == '-':
            return l - r
        elif self.operation == '*':
            return l * r
        elif self.operation == '/':
            return l / r
        elif self.operation == '^':
            return l ** r

    def __str__(self):
        return f"""{self.operation} 
        {self.left}
        {self.right}"""


