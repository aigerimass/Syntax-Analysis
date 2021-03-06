import sys
import ply.lex as lex

reserved = {
    'Main': 'MAIN',
    'Read': 'READ',
    'Write': 'WRITE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'skip': 'SKIP',
    'return': 'RETURN',
}

tokens = [
             'FUNCTION',
             'VARIABLE',
             'NUMBER',
             'STRING',
             'PLUS',
             'MINUS',
             'DIV',
             'EQUAL',
             'GT',
             'LT',
             'GEQ',
             'LEQ',
             'NEQ',
             'BINDING',
             'ROUND_OPEN_BRACKET',
             'ROUND_CLOSED_BRACKET',
             'CURLY_OPEN_BRACKET',
             'CURLY_CLOSED_BRACKET',
             'MUL',
             'AND',
             'OR',
             'POW',
             'NOT',
             'SEMICOLON',
         ] + list(reserved.values())

t_ignore = ' \n'
t_PLUS = '\+'
t_MINUS = '-'
t_DIV = r'/'
t_EQUAL = '=='
t_BINDING = '='
t_GEQ = '>='
t_NEQ = '!='
t_LEQ = '<='
t_GT = '>'
t_LT = '<'
t_ROUND_OPEN_BRACKET = r'\('
t_ROUND_CLOSED_BRACKET = r'\)'
t_CURLY_OPEN_BRACKET = r'\{'
t_CURLY_CLOSED_BRACKET = r'\}'
t_MUL = '[*]'
t_AND = '\&\&'
t_OR = r'\|\|'
t_POW = '[\^]'
t_NOT = '!'
t_SEMICOLON = ';'


def t_FUNCTION(t):
    r'[A-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'FUNCTION')
    return t


def t_NUMBER(t):
    r'[0-9]+'
    return t


def t_VARIABLE(t):
    r'[a-z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t


def t_STRING(t):
    r'"([^"\\]|\\(")?)*"(,)?'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
lexer.input(open(sys.argv[1], 'r').read())
sys.stdout = open(sys.argv[1] + '.out', 'w')

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
