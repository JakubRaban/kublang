
import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'true': 'TRUE',
    'false': 'FALSE',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    'void': 'VOID',
    'fun': 'FUN',
    'print': 'PRINT',
    'return': 'RETURN',
    'inttofloat': 'TYPECONV',
    'floattoint': 'TYPECONV'
}


tokens = [
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD', 'POWER', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'ASSIGN', 'EQ', 'NEQ',
    'LT', 'LTE', 'GT', 'GTE', 'OR', 'AND', 'COMMA', 'SEP', 'REAL', 'NUMBER', 'NAME', 'TEXT', 'NEWLINE', 'NOT', 'UMINUS'
] + list(reserved.values())


t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIV     = r'/'
t_MOD     = r'%'
t_POWER   = r'\^'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'{'
t_RBRACE  = r'}'
t_ASSIGN  = r':='
t_NOT     = r'!'
t_EQ      = r'='
t_NEQ     = r'≠'
t_LT      = r'<'
t_LTE     = r'<='
t_GT      = r'>'
t_GTE     = r'>='
t_COMMA   = r'\,'
t_SEP     = r';'


def t_OR(t):
    r"""\|\|"""
    return t


def t_AND(t):
    r"""&&"""
    return t


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


def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    t.type = reserved.get(t.value, 'NAME')
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