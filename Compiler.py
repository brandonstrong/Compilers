import ply.lex as lex
import ply.yacc as yacc

##########################################
#      Pre-amble...
##########################################

# Welcome to our compiler - python style
print("Group 0 - Sawyer Payne, Matthew Gannon, Brandon Strong")
print("Compilers are neat.")

##########################################
#      Set up lex
##########################################

# List of token names.   This is always required
tokens = (
    'INTLITERAL',
    'FLOATLITERAL',
    'STRINGLITERAL',
    'COMMENT',
    'KEYWORDS',
    'OPERATORS'
)

def printToken(TNAME, TVAL):
    print("NEW TOKEN(" + TNAME + "," + TVAL +")")

##########################################
#      Matt do these two
##########################################

# Definition for int literal
def t_INTLITERAL(t):
    # Fill in this regex (copy and paste from regex101
    r'\s\w\d'
    printToken("INTLITERAL", t.value)

# Definition for float literal
def t_FLOATLITERAL(t):
    # Fill in this regex (copy and paste from regex101
    r'\s\w\d'
    printToken("STRINGLITERAL", t.value)

##########################################
#      Sawyer do these two
##########################################

# Definition for string literal
def t_STRINGLITERAL(t):
    # Fill in this regex (copy and paste from regex101
    r'\s\w\d'
    printToken("STRINGLITERAL", t.value)

# Definition for comment
def t_COMMENT(t):
    # Fill in this regex (copy and paste from regex101
    r'\s\w\d'
    printToken("COMMENT", t.value)

##########################################
#      Brandon do these two
##########################################

# Definition for keywords
def t_KEYWORDS(t):
    # Fill in this regex (copy and paste from regex101
    r'\s\w\d'
    printToken("KEYWORDS", t.value)

# Definition for float literal
def t_OPERATORS(t):
    # Fill in this regex (copy and paste from regex101
    r'\s\w\d'
    printToken("OPERATORS", t.value)

# Error handling rule, This will tell us when an invalid token is found.
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

##########################################
#      Test out lexer
##########################################

# Test it out
data = '''
Test Str. Change L8R
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
