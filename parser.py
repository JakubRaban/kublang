
import ply.yacc as yacc

import names
from lexer import lexer, tokens

precedence = (
    ('left', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NEQ', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
    ('right', 'UMINUS'),
    ('right', 'POWER'),
    ('nonassoc', 'LPAREN', 'RPAREN')
)

class Node:
    def __init__(self, output, root, children=None):
        self.output = output
        self.root = root
        self.children = children or []

variables = names.Variables()

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


def p_input(p):
    """input : expr
             | statement"""
    p[0] = Node(p[1].output, p[1])


def p_declaration(p):
    """statement : type NAME"""
    t = to_python_type(p[1].output)
    variables.declare(p[2], t)
    p[0] = Node((), p[2])


def p_assignment(p):
    """statement : NAME ASSIGN expr"""
    variables.assign(p[1], p[3].output)
    p[0] = Node((), p[2], [p[1], p[3]])


def p_assignment_and_declaration(p):
    """statement : type NAME ASSIGN expr"""
    t = to_python_type(p[1].output)
    variables.declare(p[2], t)
    variables.assign(p[2], p[4].output)
    p[0] = Node((), p[3], [p[1], p[2], p[4]])


def p_name(p):
    """expr : NAME"""
    value = variables.get(p[1])
    p[0] = Node(value, p[1])


def p_type(p):
    """type : STRING
            | INT
            | FLOAT
            | BOOLEAN"""
    p[0] = Node(p[1], p[1])


def p_binary_math_operator(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIV expr
            | expr POWER expr"""
    if p[2] == '+':
        p[0] = Node(p[1].output + p[3].output, p[2], [p[1], p[3]])
    elif p[2] == '-':
        p[0] = Node(p[1].output - p[3].output, p[2], [p[1], p[3]])
    elif p[2] == '*':
        p[0] = Node(p[1].output * p[3].output, p[2], [p[1], p[3]])
    elif p[2] == '/':
        p[0] = Node(p[1].output / p[3].output, p[2], [p[1], p[3]])
    elif p[2] == '**':
        p[0] = Node(p[1].output ** p[3].output, p[2], [p[1], p[3]])


def p_string(p):
    """expr : TEXT"""
    p[0] = Node(p[1], p[1])


def p_number(p):
    """expr : NUMBER
            | REAL"""
    p[0] = Node(p[1], p[1])


parser = yacc.yacc()
while True:
    s = input(">>>")
    if not s:
        continue
    lexer.input(s)
    for tok in lexer:
        print(tok)
    root = parser.parse(s)
    if root is None:
        print('Error')
    else:
        print(root.output)