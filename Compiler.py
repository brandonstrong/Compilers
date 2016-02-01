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
    'FLOATLITERAL',
    'INTLITERAL',
    'STRINGLITERAL',
    'COMMENT',
    'KEYWORDS',
    'OPERATORS',
    'SPACE',
    "IDENTIFIER"
)

def printToken(TNAME, TVAL):
    print("NEW TOKEN(" + TNAME + ",'" + TVAL +"')")

# Definition for float literal
def t_FLOATLITERAL(t):
    r'(\d+\.\d+)'
    printToken("FLOATLITERAL", t.value)

# Definition for int literal
def t_INTLITERAL(t):
    r'(\d+)'
    printToken("INTLITERAL", t.value)

# Definition for string literal
def t_STRINGLITERAL(t):
    r'"[^"]+"'
    printToken("STRINGLITERAL", t.value)

# Definition for comment
def t_COMMENT(t):
    r'--.*'
    printToken("COMMENT", t.value)

# Definition for keywords
def t_KEYWORDS(t):
    r'(PROGRAM)|(BEGIN)|(END)|(FUNCTION)|(READ)|(WRITE)|(IF)|(ELSE)|(ENDIF)|(WHILE)|(ENDWHILE)|(CONTINUE)|(BREAK)|(RETURN)|(INT)|(VOID)|(STRING)|(FLOAT)'
    printToken("KEYWORDS", t.value)

# Definition for float literal
def t_OPERATORS(t):
    r'(:=)|(!=)|(<=)|(>=)|(>)|(<)|(\+)|(-)|(\*)|(\/)|(=)|(\()|(\))|(;)|(,)'
    printToken("OPERATORS", t.value)
# Handle spaces
def t_SPACE(t):
    r'\s'
    # Do nothing with spaces.

# Definition for variables
def t_IDENTIFIER(t):
    r'\w+'
    printToken("IDENTIFIER", t.value)


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
PROGRAM fibonacci
BEGIN
    -- test 11
    INT stuff = dsfa12345asdfa;
    FLOAT flo = sdf123.4456asdf
	STRING inputs := "Please input an integer number: ";
	STRING space := " ";
	STRING eol := "\n";

	FUNCTION INT F (INT n)
	BEGIN

		IF (n > 2)
		     RETURN F(n-1)+F(n-2);
		ELSE
			RETURN 1;
	    ENDIF
	END
    -- testing theiss flkja 2 342235 532.33


	FUNCTION VOID main ()
	BEGIN
		INT i, end, result;
		WRITE(input);
		READ(end);

	i := 0;
	WHILE (i != end)
		result := F(i);
		WRITE (i,space);
		WRITE (result,eol);
		i := i + 1;
	ENDWHILE

	END

END
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
