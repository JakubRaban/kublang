
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


def p_input(p):
    """input : expr
             | statement"""
    p[0] = ast.Input(p[1])


def p_parentheses(p):
    """expr : LPAREN expr RPAREN"""
    p[0] = p[2]


def p_declaration(p):
    """statement : type NAME"""
    p[0] = ast.Declaration(p[1], ast.VariableName(p[2]))


def p_assignment(p):
    """statement : NAME ASSIGN expr"""
    p[0] = ast.Assignment(ast.VariableName(p[1]), p[3])


def p_assignment_and_declaration(p):
    """statement : type NAME ASSIGN expr"""
    p[0] = ast.DeclarationWithAssignment(p[1], ast.VariableName(p[2]), p[4])


def p_binary_math_operator(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIV expr
            | expr POWER expr"""
    p[0] = ast.BinaryMathOperator(p[2], p[1], p[3])


def p_binary_logical_operator(p):
    """expr : expr AND expr
            | expr OR expr"""
    p[0] = ast.BinaryLogicalOperator(p[2], p[1], p[3])


def p_unary_logical_operator(p):
    """expr : NOT expr"""
    p[0] = ast.UnaryLogicalOperator(p[1], p[2])


def p_comparison(p):
    """expr : expr EQ expr
            | expr NEQ expr
            | expr GT expr
            | expr GTE expr
            | expr LT expr
            | expr LTE expr"""
    p[0] = ast.Comparison(p[2], p[1], p[3])


def p_if(p):
    """statement : IF LPAREN expr RPAREN LBRACE input RBRACE"""
    p[0] = ast.IfStatement(p[3], p[6])


def p_while(p):
    """statement : WHILE LPAREN expr RPAREN LBRACE input RBRACE"""
    p[0] = ast.WhileStatement(p[3], p[6])


def p_string(p):
    """expr : TEXT"""
    p[0] = ast.String(p[1])


def p_number(p):
    """expr : NUMBER
            | REAL"""
    p[0] = ast.Number(p[1])


def p_name(p):
    """expr : NAME"""
    p[0] = ast.VariableRead(p[1])


def p_boolean(p):
    """expr : TRUE
            | FALSE"""
    p[0] = ast.TrueOrFalse(p[1])


def p_type(p):
    """type : STRING
            | INT
            | FLOAT
            | BOOLEAN"""
    p[0] = ast.TypeName(p[1])


parser = yacc.yacc()
variables = names.VariableArray()
while True:
    s = input('>>> ')
    # lexer.input(s)
    # for tok in lexer:
    #     print(tok)
    if s:
        root = parser.parse(s)
        print(root)
        print('Result:', root.evaluate(variables))
