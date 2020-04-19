
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
    ('left', 'TIMES', 'DIV', 'MOD'),
    ('right', 'UMINUS'),
    ('right', 'POWER'),
    ('nonassoc', 'LPAREN', 'RPAREN'),
    ('nonassoc', 'SEP')
)

class Node:
    def __init__(self, output, root, children=None):
        self.output = output
        self.root = root
        self.children = children or []


def p_input(p):
    """program : statements"""
    p[0] = ast.Program(p[1])


def p_lines(p):
    """statements : statements statement
                  | statement"""
    if len(p) == 3:
        p[0] = ast.Lines(p[1].lines + [p[2]])
    else:
        p[0] = ast.Lines([p[1]])


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
            | expr POWER expr
            | expr MOD expr"""
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
    """statement : IF LPAREN expr RPAREN LBRACE statements RBRACE"""
    p[0] = ast.IfStatement(p[3], p[6])


def p_if_else(p):
    """statement : IF LPAREN expr RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE"""
    p[0] = ast.IfElseStatement(p[3], p[6], p[10])


def p_while(p):
    """statement : WHILE LPAREN expr RPAREN LBRACE statements RBRACE"""
    p[0] = ast.WhileStatement(p[3], p[6])


def p_type_conversion(p):
    """expr : TYPECONV LPAREN expr RPAREN"""
    if p[1] == 'inttofloat':
        p[0] = ast.IntToFloat(p[3])
    elif p[1] == 'floattoint':
        p[0] = ast.FloatToInt(p[3])


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


def p_print(p):
    """statement : PRINT LPAREN expr RPAREN"""
    p[0] = ast.Print(p[3])


parser = yacc.yacc()
variables = names.VariableArray()
# with open('collatz.orl', 'r') as f:
#     program = f.read()
while True:
    program = ''
    while line := input('>>> '):
        program += line + '\n'
    # lexer.input(program)
    # for tok in lexer:
    #     print(tok)
    # print(program)
    if program:
        root = parser.parse(program)
        print(root)
        root.evaluate(variables)
