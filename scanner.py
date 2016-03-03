import ply.lex as lex
import sys, getopt


##########################################
#  CSCI-468 Compiler
#  Group 0 - Brandon Strong, Sawyer Payne,
#  and Matthew Gannon
#  Part 1 - Create a scanner which will
#  create tokens from the Little language
#  to pass to the parser.
#
##########################################


##########################################
#      Set up inputs
##########################################
filename = sys.argv[1]
f = open(filename, "r")
data = f.read()

##########################################
#      Set up lex
##########################################

# List of token names.   This is always required
tokens = (
    'FLOATLITERAL',
    'INTLITERAL',
    'STRINGLITERAL',
    'COMMENT',
    'SPACE',
    "IDENTIFIER",

    "PROGRAM",
    "FUNCTION",
    "BEGIN",
    "READ",
    "WRITE",
    "IF",
    "ELSE",
    "ENDIF",
    "WHILE",
    "ENDWHILE",
    "CONTINUE",
    "BREAK",
    "RETURN",
    "INT",
    "VOID",
    "STRING",
    "FLOAT",
    "END",

    "ASSIGN",
    "NOTEQUAL",
    "LESSEQUAL",
    "GREATEQUAL",
    "GREATER",
    "LESS",
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "EQUAL",
    "LPAREN",
    "RPAREN",
    "SEMICOLON",
    "COMMA"
)
t_ASSIGN = r':='
t_NOTEQUAL = r'!='
t_LESSEQUAL = r'<='
t_GREATEQUAL = r'>='
t_GREATER = r'>'
t_LESS = r'<'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUAL = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','

def printToken(TNAME, TVAL):
    i = 0 # This is placeholder so we can have the method. It does nothing important. Don't worry about it.
    # print("Token Type: " + TNAME + "\nValue: " + TVAL.replace("\n", "\\n"))

# Definition for float literal
def t_FLOATLITERAL(t):
    r'(\d+\.\d+)'
    printToken("FLOATLITERAL", t.value)
    return t

# Definition for int literal
def t_INTLITERAL(t):
    r'(\d+)'
    printToken("INTLITERAL", t.value)
    return t

# Definition for string literal
def t_STRINGLITERAL(t):
    r'"[^"]+"'
    printToken("STRINGLITERAL", t.value)
    return t

# Definition for comment
def t_COMMENT(t):
    r'''--.*'''
    # Do nothing with spaces.

# Handle spaces
def t_SPACE(t):
    r'\s'
    # Do nothing with spaces.


# Definition for variables
def t_IDENTIFIER(t):
    r'\w+'
    if t.value in tokens:
        t.type = t.value
        printToken(t.type, t.value)
    else:
        printToken("IDENTIFIER", t.value)
    return t


# Error handling rule, This will tell us when an invalid token is found.
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

##########################################
#      Test out lexer
##########################################

# Give the lexer some input
lexer.input(data)
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    #print(tok)
