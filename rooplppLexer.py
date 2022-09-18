import ply.lex as lex

tokens = (
    'NUMBER',
    'ID',
    'CONST',
    'STRING',
    'MUL',
    'DIV',
    'MOD',
    'ADD',
    'SUB',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQ',
    'NE',
    'BAND',
    'XOR',
    'BOR',
    'AND',
    'OR',
    'SWAP',
    'COMMA',
    'WDOT',
    'WCOLON',
    'MODADD',
    'MODSUB',
    'MODXOR',
    'DOT',
    'COLON',
    'LPAREN',
    'RPAREN',
    'LBRA',
    'RBRA',
    'CLASS',
    'INHERITS',
    'METHOD',
    'CALL',
    'UNCALL',
    'CONSTRUCT',
    'DESTRUCT',
    'SKIP',
    'FROM',
    'DO',
    'LOOP',
    'UNTIL',
    'FOR',
    'IN',
    'END',
    'SWITCH',
    'HCTIWS',
    'CASE',
    'FCASE',
    'ECASE',
    'ESAC',
    'BREAK',
    'DEFAULT',
    'INT',
    'NIL',
    'IF',
    'THEN',
    'ELSE',
    'FI',
    'LOCAL',
    'DELOCAL',
    'NEW',
    'DELETE',
    'COPY',
    'UNCOPY',
    'SHOW',
    'PRINT',
    'EOF',
    'PLUS',
    'TIMES',
    'MINUS',
    'DIVIDE',
    'LBRACE',
    'RBRACE',
)

reserved = {
  'class' : 'CLASS',
  'if'    : 'IF',
  'then'  : 'THEN',
  'else'  : 'ELSE',
  'while' : 'WHILE',
  'main' : 'MAIN',
  'method' : 'METHOD',
  'int': 'INT',
}

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_CLASS= 'class'
t_METHOD= 'method'
t_IF= 'method'
t_COLON = ':'
t_ADD= r'\+'
t_MODADD= r'\+='
t_MODSUB= r'-='
t_MODXOR= r'^='
t_SUB= r'-'
t_MUL= r'\*'
t_DIV= r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NUMBER = '[0-9.edED+-]+'
t_LBRACE = '{'
t_RBRACE = '}'
# A string containing ignored characters (spaces and tabs)
t_ignore_COMMENT = r'//.*'
t_ignore = ' \t'
# A regular expression rule with some action code



# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


def lex_test():
    f = open('data.txt', 'r')
    data = f.read()
    f.close()

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    print(lexer.lineno)


if __name__ == '__main__':
    lex_test()
