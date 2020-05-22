
reserved = {
        'solve' : 'SOLVE',
}

tokens = [
        'PLUS',
        'MINUS',
        'DEQ',
        'EQ',
        'NE',
        'GT',
        'GE',
        'LT',
        'LE',
        'LBRACKET',
        'RBRACKET',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'COMMA',
        'COLON',
        'DOT',
        'NUM',
        'ID',
]
tokens += list(reserved.values())

t_PLUS   = r'\+'
t_MINUS = r'-'
t_DEQ = r'=='
t_EQ = r'='
t_NE = r'!='
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_COMMA = r','
t_COLON = r':'
t_DOT = r'\.'

t_ignore_COMMENT = r'\#.*'
t_ignore = ' \t\r\f\v'

def t_NUM(t):
    r'\d'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f'Unrecognized character "{t.value}" at line {t.lineno}')
    t.lexer.skip(1)
