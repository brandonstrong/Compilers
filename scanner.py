import ply.lex as lex
import sys, getopt


##########################################
#  CSCI-468 Compiler
#  Group 0 - Brandon Strong, Sawyer Payne,
#  and Matthew Gannon
#  Project 1 - Create a scanner which will
#  create tokens from the Little language
#  to pass to the parser.
#
##########################################


##########################################
#      Set up inputs
##########################################
#filename = sys.argv[1]
#f = open(filename,"r")
#data = f.read()
data = '''
PROGRAM fibonacci
BEGIN

	STRING input := "Please input an integer number: ";
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
    i = 0
    #print("Token Type: " + TNAME + "\nValue: " + TVAL.replace("\n", "\\n"))

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
    r'--.*'
    # Do nothing with spaces.

# Definition for keywords
def t_KEYWORDS(t):
    r'(PROGRAM)|(BEGIN)|(FUNCTION)|(READ)|(WRITE)|(IF)|(ELSE)|(ENDIF)|(WHILE)|(ENDWHILE)|(CONTINUE)|(BREAK)|(RETURN)|(INT)|(VOID)|(STRING)|(FLOAT)|(END)'
    printToken("KEYWORD", t.value)
    return t

# Definition for float literal
def t_OPERATORS(t):
    r'(:=)|(!=)|(<=)|(>=)|(>)|(<)|(\+)|(-)|(\*)|(\/)|(=)|(\()|(\))|(;)|(,)'
    printToken("OPERATOR", t.value)
    return t

# Handle spaces
def t_SPACE(t):
    r'\s'
    # Do nothing with spaces.

# Definition for variables
def t_IDENTIFIER(t):
    r'\w+'
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
    print(tok)
