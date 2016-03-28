import ply.yacc as yacc
from scanner import tokens
from collections import deque
from collections import OrderedDict
import sys
from scanner import tokens

class Symbol:
    def __init__(self):
        self.data = []

    name = ""
    type = ""
    value = ""

class Node:

    def __init__(self):
        self.data = []

    children = []
    symbols = []
    scopeLevel = 0
    parent = None
    name = ""

# Block and scope level numeric trackers
blockCount = 0
currentScope = 0

# Create root GLOBAL node
root = Node()
root.scopeLevel = currentScope
root.parent = root
root.name = "GLOBAL"

# Set current node and symbol
curnode = root
cursymbol = Symbol()

# Stack for keeping track of variable, function, and program names
idnames = []

# List for tracking function parameter variables
paramSymbols = []
reverseSymbols = []

# Boolean indication of whether program passed or not
accepted = True

# Program
def p_program_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    pass


def p_program_idea(p):
    'id : IDENTIFIER'
    global idnames
    idnames.append(p.slice[1].value)
    pass

def p_program_pgm_body(p):
    'pgm_body : decl func_declarations'
    pass

def p_program_decl(p):
    '''decl : string_decl decl
    | var_decl decl
    | empty'''
    pass

# Global String

def p_gstring_string_decl(p):
    '''string_decl : STRING id ASSIGN str SEMICOLON'''
    pass

def p_gstring_str(p):
    'str : STRINGLITERAL'

    # Declare global variables
    global curnode
    global idnames

    # Create new symbol
    thissymbol = Symbol()
    thissymbol.name = idnames.pop()
    thissymbol.type = "STRING"
    thissymbol.value = p.slice[1].value

    # Add symbol to current node
    curnode.symbols = curnode.symbols + [thissymbol]
    pass

# Variables

def p_variables_var_decl(p):
    'var_decl : var_type id_list SEMICOLON'
    pass

def p_variables_var_type(p):
    '''var_type : FLOAT
    | INT'''

    # Define global variables
    global cursymbol

    # Set cursymbol data type
    cursymbol.type = p.slice[1].type

    pass

def p_variables_any_type(p):
    '''any_type : var_type
    | VOID'''
    pass

def p_variables_id_list(p):
    '''id_list : id id_tail'''

    # Define global variables
    global reverseSymbols
    global curnode

    # Add reverse symbols to curnode symbols and clear reverse symbols
    reverseSymbols.reverse()
    curnode.symbols = curnode.symbols + reverseSymbols
    reverseSymbols = []

    pass

def p_variables_id_tail(p):
    '''id_tail : COMMA id id_tail
    | empty'''

    # Define global variables
    global reverseSymbols
    global cursymbol
    global idnames

    # Create new symbol
    thissymbol = Symbol()
    thissymbol.name = idnames.pop()
    thissymbol.type = cursymbol.type

    # Add symbol to curnode
    reverseSymbols = reverseSymbols + [thissymbol]

    pass

# Function parameter list

def p_fparams_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
    | empty'''

    # Declare global variables
    global currentScope
    global paramSymbols
    global curnode
    global idnames

    # Increment scope
    currentScope += 1

    # Create new node
    thisnode = Node()
    thisnode.scopeLevel = currentScope
    thisnode.name = idnames.pop()
    thisnode.parent = curnode

    # Switch current node to this node
    curnode.children = curnode.children + [thisnode]

    # Set current node
    curnode = thisnode

    # Set current node symbols from parameters and reset paramsymbols
    curnode.symbols = curnode.symbols + paramSymbols
    paramSymbols = []

    pass

def p_fparams_param_decl(p):
    'param_decl : var_type id'

    # Define global variables
    global paramSymbols
    global cursymbol
    global idnames

    # Create new symbol
    thissymbol = Symbol()
    thissymbol.name = idnames.pop()
    thissymbol.type = cursymbol.type

    # Add symbol to paramSymbols
    paramSymbols = paramSymbols + [thissymbol]

    pass

def p_fparams_param_decl_tail(p):
    '''param_decl_tail : COMMA param_decl param_decl_tail
    | empty'''
    pass

# Function declaration list

def p_fdecl_func_declarations(p):
    '''func_declarations : func_decl func_declarations
    | empty'''
    pass

def p_fdecl_func_decl(p):
    'func_decl : FUNCTION any_type id LPAREN param_decl_list RPAREN BEGIN func_body END'

    # Declare global variables
    global currentScope
    global curnode

    # Decrement scope and set curnode to parent
    currentScope -= 1
    curnode = curnode.parent

    pass

def p_fdecl_func_body(p):
    'func_body : decl stmt_list'
    pass

# Statement list

def p_statements_stmt_list(p):
    '''stmt_list : stmt stmt_list
    | empty'''
    pass

def p_statements_stmt(p):
    '''stmt : base_stmt
    | if_stmt
    | while_stmt'''
    pass

def p_statements_base_stmt(p):
    '''base_stmt : assign_stmt
    | read_stmt
    | write_stmt
    | return_stmt'''
    pass

# Basic statements
def p_basic_assign_stmt(p):
   'assign_stmt : assign_expr SEMICOLON'
   pass

def p_basic_assign_expr(p):
   'assign_expr : id ASSIGN expr'
   pass

def p_basic_read_stmt(p):
   'read_stmt : READ LPAREN id_list RPAREN SEMICOLON'

   # Declare global variable
   global idnames

   # Consume symbol from curnode
   curnode.symbols.pop()

   pass

def p_basic_write_stmt(p):
   'write_stmt : WRITE LPAREN id_list RPAREN SEMICOLON'

   # Declare global variable
   global curnode

   # Consume symbol from curnode
   curnode.symbols.pop()

   pass

def p_basic_return_stmt(p):
   'return_stmt : RETURN expr SEMICOLON'
   pass


# Expressions List

def p_expressions_expr(p):
    '''expr : expr_prefix factor'''
    pass

def p_expressions_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
    | empty'''
    pass

def p_expressions_factor(p):
    'factor : factor_prefix postfix_expr'
    pass

def p_expressions_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
    | empty'''
    pass

def p_expressions_postfix_expr(p):
    '''postfix_expr : primary
    | call_expr'''
    pass

def p_expressions_call_expr(p):
    'call_expr : id LPAREN expr_list RPAREN'
    pass

def p_expressions_expr_list(p):
    '''expr_list : expr expr_list_tail
    | empty'''
    pass

def p_expressions_expr_list_tail(p):
    '''expr_list_tail : COMMA expr expr_list_tail
    | empty'''
    pass

def p_expressions_primary(p):
    '''primary : LPAREN expr RPAREN
    | id
    | INTLITERAL
    | FLOATLITERAL'''
    pass

def p_expressions_addop(p):
    '''addop : PLUS
    | MINUS'''
    pass

def p_expressions_mulop(p):
    '''mulop : MULTIPLY
    | DIVIDE'''
    pass

# Complex Statemetns
def p_complex_if_stmt(p):
   'if_stmt : IF LPAREN cond RPAREN decl stmt_list else_part ENDIF'

   # Declare global variables
   global curnode
   global currentScope

   # move current scope back one and decrease current node by one
   curnode = curnode.parent
   currentScope -= 1

   pass

def p_complex_else_part(p):
   '''else_part : ELSE decl stmt_list
   | empty'''

   if(len(p.slice) == 4):
       # Declare global variables
       global curnode
       global blockCount
       global currentScope

       # Increment block count
       blockCount += 1

       # Switch current node to parent
       curnode = curnode.parent

       # Create new node
       thisnode = Node()
       thisnode.scopeLevel = currentScope
       thisnode.name = "Block" + str(blockCount)
       thisnode.parent = curnode

       # Add thisnode to curnode children
       curnode.children = curnode.children + [thisnode]

       # Switch current node to this node
       curnode = thisnode

   pass

def p_complex_cond(p):
   '''cond : expr compop expr'''

   # Declare global variables
   global blockCount
   global currentScope
   global curnode
   global idnames

   # Increment scope and block count
   currentScope += 1
   blockCount += 1

   # Create new node
   thisnode = Node()
   thisnode.scopeLevel = currentScope
   thisnode.name = "Block" + str(blockCount)
   thisnode.parent = curnode

   # Add this node to current node children
   curnode.children = curnode.children + [thisnode]

    # Switch current node to this node
   curnode = thisnode
   pass

def p_complex_compop(p):
    '''compop : LESS
    | GREATER
    | EQUAL
    | NOTEQUAL
    | LESSEQUAL
    | GREATEQUAL'''
    pass
# While statement

def p_whilestatement_while_stmt(p):
    'while_stmt : WHILE LPAREN cond RPAREN decl stmt_list ENDWHILE'

    # Declare global variables
    global curnode
    global currentScope

    # move current scope back one and decrease current node by one
    curnode = curnode.parent
    currentScope -= 1

    pass

# Empty
def p_empty(p):
    'empty :'
    pass

# Error handling
def p_error(p):
    global accepted
    accepted = False
    pass

# Print off symbol tables for scopes
def treeTraversal(node):
    # Print root node information
    printinfo(node)

    # Traverse the rest of the tree and print off information
    for n in node.children:
        treeTraversal(n)

# Print information for node
def printinfo(node):
    # Print node name
    print("Symbol table " + node.name)

    # Iterate through each symbol and print it off
    for s in node.symbols:
        # Print symbol name and type
        str = "name " + s.name + " type " + s.type

        # Only print symbol value if it exists
        if (s.value != ""):
            str = str + " value " + s.value
        print (str)
    print()

# Get input
#filename = sys.argv[1]
#f = open(filename,"r")
#data = f.read()
data = '''
PROGRAM fibonacci
BEGIN

	STRING dummy := "abcde";

	INT i,result;


	FUNCTION INT F (INT n)
	BEGIN

		IF (n > 2)
			RETURN F(n-1)+F(n-2);
		ENDIF
		IF (n = 0)   --This is a comment
			RETURN 0;
        ELSE
			RETURN 1;
		ENDIF
	END


	FUNCTION VOID main ()
	BEGIN

    INT i, end, result;
		READ(end);

	i := 0;
 	WHILE (i != end)
		result := F(i);
		WRITE (i);
		WRITE (result);
		i := i + 1;
	ENDWHILE


	END

END

'''

# Build parser and parse data
parser = yacc.yacc()
result = parser.parse(data)

# Traverse tree
treeTraversal(root)

if(accepted):
    print("Accepted")
else:
    print("Not accepted")

