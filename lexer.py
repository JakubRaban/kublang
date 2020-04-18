
import ply.lex as lex

tokens = [
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'POWER', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'ASSIGN', 'EQ', 'NEQ',
    'LT', 'LTE', 'GT', 'GTE', 'OR', 'AND', 'COMMA', 'SEP', 'IF', 'ELSE', 'FUN', 'WHILE', 'INT', 'BOOLEAN', 'STRING',
    'PRINT', 'REAL', 'NUMBER', 'NAME', 'TEXT', 'TRUE', 'FALSE', 'NEWLINE', 'NOT', 'UMINUS', 'FLOAT'
]

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIV     = r'/'
t_POWER   = r'\*\*'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'{'
t_RBRACE  = r'}'
t_ASSIGN  = r'='
t_NOT     = r'!'
t_EQ      = r'=='
t_NEQ     = r'!='
t_LT      = r'<'
t_LTE     = r'<='
t_GT      = r'>'
t_GTE     = r'>='
t_OR      = r'\|\|'
r_AND     = r'&&'
t_COMMA   = r'\,'


def t_REAL(t):
    r"""(\d+\.\d+)|(\d+\.)|(\.\d+)"""
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_TEXT(t):
    r"""\"(.*?)\""""
    t.value = str(t.value[1:-1])
    return t


def t_IF(t):
    r"""if"""
    return t


def t_ELSE(t):
    r"""else"""
    return t


def t_FUN(t):
    r"""fun"""
    return t


def t_WHILE(t):
    r"""while"""
    return t


def t_BOOLEAN(t):
    r"""boolean"""
    return t


def t_INT(t):
    r"""int"""
    return t


def t_STRING(t):
    r"""string"""
    return t


def t_FLOAT(t):
    r"""float"""
    return t


def t_PRINT(t):
    r"""print"""
    return t


def t_TRUE(t):
    r"""true"""
    return t


def t_FALSE(t):
    r"""false"""
    return t


def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    return t


def t_NEWLINE(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = " \t"


lexer = lex.lex()


# def process_tokens():
#     data = '''
#     while(3+i>=2) { print("xd") }
#     ej = 3+2
#      '''
#     global lexer
#     lexer.input(data)
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break  # No more input
#         print(tok)
#
# process_tokens()