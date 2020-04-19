
import ply.yacc as yacc

import ast
import names
from lexer import lexer, tokens
from helpers import *

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

variables = names.VariableArray()


def p_input(p):
    """input : expr"""
    p[0] = Node(p[1].output, p[1])


def p_parentheses(p):
    """expr : LPAREN expr RPAREN"""
    p[0] = Node(p[2].output, p[2])


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


def p_binary_math_operator(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIV expr
            | expr POWER expr"""
    p[0] = ast.BinaryOperator(p[2], p[1], p[3])


def p_binary_logical_operator(p):
    """expr : expr AND expr
            | expr OR expr"""
    left, right = p[1].output, p[3].output
    check_boolean_type(left, right)
    if p[2] == '&&':
        p[0] = Node(left and right, p[2], [p[1], p[3]])
    elif p[2] == '||':
        p[0] = Node(left or right, p[2], [p[1], p[3]])


def p_unary_logical_operator(p):
    """expr : NOT expr"""
    operand = p[2].output
    p[0] = Node(not operand, p[1], [p[2]])


def p_comparison(p):
    """expr : expr EQ expr
            | expr NEQ expr
            | expr GT expr
            | expr GTE expr
            | expr LT expr
            | expr LTE expr"""
    left, right = p[1].output, p[3].output
    check_numeric_type(left, right)
    if p[2] == '=':
        p[0] = Node(left == right, p[2], [p[1], p[3]])
    elif p[2] == '≠':
        p[0] = Node(left != right, p[2], [p[1], p[3]])
    elif p[2] == '>=':
        p[0] = Node(left >= right, p[2], [p[1], p[3]])
    elif p[2] == '>':
        p[0] = Node(left > right, p[2], [p[1], p[3]])
    elif p[2] == '<=':
        p[0] = Node(left <= right, p[2], [p[1], p[3]])
    elif p[2] == '<':
        p[0] = Node(left < right, p[2], [p[1], p[3]])


def p_if(p):
    """statement : IF LPAREN expr RPAREN LBRACE input RBRACE"""
    check_boolean_type(p[3].output)
    if p[3].output:
        p[0] = Node(p[6].output, p[1], [p[3], p[6]])
    else:
        p[0] = Node((), p[1])


def p_string(p):
    """expr : TEXT"""
    p[0] = Node(p[1], p[1])


def p_number(p):
    """expr : NUMBER
            | REAL"""
    p[0] = ast.Number(p[1])


def p_name(p):
    """expr : NAME"""
    value = variables.get(p[1])
    p[0] = Node(value, p[1])


def p_boolean(p):
    """expr : TRUE
            | FALSE"""
    p[0] = Node(p[1], p[1])


def p_type(p):
    """type : STRING
            | INT
            | FLOAT
            | BOOLEAN"""
    p[0] = Node(p[1], p[1])


parser = yacc.yacc()
while True:
    s = input(">>> ")
    if not s:
        continue
    lexer.input(s)
    for tok in lexer:
        print(tok)
    root = parser.parse(s)
    print(root.children)
    if root is None:
        print('Compiler error')
    else:
        print(root.output)