
import ply.yacc as yacc
from lex import tokens
import ast

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
    """statement : type NAME
                 | GLOBAL type NAME"""
    if len(p) == 3:
        p[0] = ast.Declaration(p[1], ast.VariableName(p[2]), is_global=False)
    else:
        p[0] = ast.Declaration(p[2], ast.VariableName(p[3]), is_global=True)


def p_assignment(p):
    """statement : NAME ASSIGN expr"""
    p[0] = ast.Assignment(ast.VariableName(p[1]), p[3])


def p_assignment_and_declaration(p):
    """statement : type NAME ASSIGN expr
                 | GLOBAL type NAME ASSIGN expr"""
    if len(p) == 5:
        p[0] = ast.DeclarationWithAssignment(p[1], ast.VariableName(p[2]), p[4], is_global=False)
    else:
        p[0] = ast.DeclarationWithAssignment(p[2], ast.VariableName(p[3]), p[5], is_global=True)


def p_binary_math_operator(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIV expr
            | expr POWER expr
            | expr MOD expr"""
    optimized = False
    if p[2] == '/':
        optimized = True
        if isinstance(p[3], ast.Number) and p[3].value == 1:
            p[0] = p[1]
        else:
            optimized = False
    elif p[2] == '*':
        optimized = True
        if isinstance(p[3], ast.Number):
            if p[3].value == 1:
                p[0] = p[1]
            elif p[3].value == 2:
                p[0] = ast.BinaryMathOperator('+', p[1], p[1])
        elif isinstance(p[1], ast.Number):
            if p[1].value == 1:
                p[0] = p[3]
            elif p[1].value == 2:
                p[0] = ast.BinaryMathOperator('+', p[3], p[3])
        else:
            optimized = False
    elif p[2] == '+':
        optimized = True
        if isinstance(p[3], ast.Number) and p[3].value == 0:
            p[0] = p[1]
        elif isinstance(p[1], ast.Number) and p[1].value == 0:
            p[0] = p[3]
        else:
            optimized = False
    elif p[2] == '-' and isinstance(p[3], ast.Number) and p[3].value == 0:
        p[0] = p[1]
        optimized = True
    elif p[2] == '^' and isinstance(p[3], ast.Number) and p[3].value == 2:
        p[0] = ast.BinaryMathOperator('*', p[1], p[1])
        optimized = True
    if not optimized:
        p[0] = ast.BinaryMathOperator(p[2], p[1], p[3])


def p_unary_math_operator(p):
    """expr : MINUS expr %prec UMINUS"""
    p[0] = ast.UnaryMathOperator(p[1], p[2])


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


def p_function_declaration(p):
    """statement : type NAME LPAREN arglist RPAREN LBRACE statements RBRACE"""
    p[0] = ast.FunctionDeclaration(ast.VariableName(p[2]), p[4], p[7], p[1])


def p_function_call(p):
    """statement : NAME LPAREN exprlist RPAREN"""
    p[0] = ast.FunctionCall(ast.VariableName(p[1]), p[3])


def p_function_call_expr(p):
    """expr : NAME LPAREN exprlist RPAREN"""
    p[0] = ast.FunctionCall(ast.VariableName(p[1]), p[3])


def p_expression_list(p):
    """exprlist : exprlist COMMA expr
                | expr"""
    if len(p) == 4:
        p[0] = ast.FunctionCallArguments(p[1].arguments + [p[3]])
    else:
        p[0] = ast.FunctionCallArguments([p[1]])


def p_expression_list_empty(p):
    """exprlist :"""
    p[0] = ast.FunctionCallArguments([])


def p_return(p):
    """statement : RETURN expr"""
    p[0] = ast.ReturnStatement(p[2])


def p_argument_list(p):
    """arglist : arglist COMMA arg
               | arg"""
    if len(p) == 4:
        p[0] = ast.FunctionArguments(p[1].arguments + [p[3]])
    else:
        p[0] = ast.FunctionArguments([p[1]])


def p_empty_argument_list(p):
    """arglist :"""
    p[0] = ast.FunctionArguments([])


def p_argument(p):
    """arg : type NAME"""
    p[0] = ast.FunctionArgument(p[1], ast.VariableName(p[2]))


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
            | BOOLEAN
            | VOID"""
    p[0] = ast.TypeName(p[1])


def p_print(p):
    """statement : PRINT LPAREN expr RPAREN"""
    p[0] = ast.Print(p[3])


parser = yacc.yacc()
