import ply.yacc as yacc
from scanner import tokens
from collections import deque
from collections import OrderedDict
import sys
from scanner import tokens


# Class for variable or sym
class Symbol:

    # Initialize
    def __init__(self):
        self.data = []

    # The values of each symbol or variable
    name = ""
    type = ""
    value = ""

# IR Operation node
class OpNode:
    def __init__(self, name, op1, op2, result, label, string):
        self.data = []
        self.name = name
        self.op1 = op1
        self.op2 = op2
        self.result = result
        self.label = label
        self.string = string


# Class for each node in the tree or scope
class Node:

    # Initialize
    def __init__(self):
        self.data = []

    # List of children nodes and symbols
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
reversPrevSize = 0

# Boolean indication of whether program passed or not
accepted = True

# String that will be printed at end
printstr = ""

# variables for IR
irString = ';IR code\n'
irlabel = 1
regCounter = 1
optype = ''
opList = []
registerNums = 0

def newRegs(oldreg):
    global registerNums
    registerNums = registerNums + 1
    registerName ="r" + registerNums

    return registerName


def convert():
    global irString
    #assemble = [irString.replace(";", "") for clean in irString.split('\n') if irString.replace()]
    # myOp = OpNode()

    # Vars and Strs must precede all codes and labels in tiny assembly
    # The only ops on string constants is sys writes sid
    # strings can include \n for end-of-line

    myVars = []
    myStrs = []
    regDict ={}

    assembled = "fuck this"

    # new temporary numbers for Tiny ASS


    global opList
# need to change all temporary variables into registers.

    for thisOp in opList:

        # integer addition, reg = reg + op1
        if thisOp.name == 'ADDI':
            i = 10
        #
        elif thisOp.name == 'ADDF':
            i = 10
        elif thisOp.name == 'SUBI':
            i = 10

        elif thisOp.name == 'SUBF':
            i = 10

        elif thisOp.name == 'MULTI':
            i = 10

        elif thisOp.name == 'MULTF':
            i = 10

        elif thisOp.name == 'DIVI':
            i = 10
        elif thisOp.name == 'DIVF':
            i = 10
        elif thisOp.name == 'STOREI':
            i = 10

        elif thisOp.name == 'STOREF':
            i = 10
        elif thisOp.name == 'GT':
            i = 10

        elif thisOp.name == 'GE':
            i = 10
        elif thisOp.name == 'LT':
            i = 10

        elif thisOp.name == 'LE':
            i = 10
        elif thisOp.name == 'NE':
            i = 10

        elif thisOp.name == 'EQ':
            i = 10

        elif thisOp.name == 'JUMP':
            i = 10
        elif thisOp.name == 'LABEL':
            i = 10

        elif thisOp.name == 'READI':
            i = 10

        elif thisOp.name == 'READF':
            i = 10

        elif thisOp.name == 'WRITEI':
            i = 10

        elif thisOp.name == 'WRITEF':
            i = 10

    return assembled



# Program
def p_program_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    pass


# Identifiers
def p_program_idea(p):
    'id : IDENTIFIER'
    global idnames
    idnames.append(p.slice[1].value)
    p[0]=p[1]
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
    global optype
    optype = 'S'
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
    global reversPrevSize

    # Add reverse symbols to curnode symbols and clear reverse symbols
    reverseSymbols.reverse()
    curnode.symbols = curnode.symbols + reverseSymbols
    reversPrevSize = len(reverseSymbols)
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
    if thissymbol.name == 'newline':
        thissymbol.type = 'STRING'
        thissymbol.value = '\n'
    else:
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
    global irString
    global opList

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

    # Add text to irString
    irString += ";LABEL " + thisnode.name + "\n;Link"
    opList += [OpNode('LABEL', '', '', '', '', thisnode.name)]
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
    global irString
    global opList
    irString += '\n;STORE' + optype + ' ' +  p[3] + " " + p[1]
    opList += [OpNode('STORE' + optype, p[3], '', p[1], '', '')]
    pass


def p_basic_read_stmt(p):
    'read_stmt : READ LPAREN id_list RPAREN SEMICOLON'

    # Declare global variable
    global idnames
    global reversPrevSize
    global irString
    global optype
    global opList

    i = 0
    while i < reversPrevSize:
        i += 1
        # Consume symbol from curnode
        thissym = curnode.symbols.pop()
        irString +='\n;READ' + optype + ' ' + thissym.name
        opList += [OpNode('READ' + optype, '', '', thissym.name, '', '')]
    pass


def p_basic_write_stmt(p):
    'write_stmt : WRITE LPAREN id_list RPAREN SEMICOLON'

    # Declare global variable
    global curnode
    global reversPrevSize
    global irString
    global idnames
    global optype
    global opList

    i = 0
    writestr = ''
    minilist = []
    while i < reversPrevSize:
        i += 1
        # Consume symbol from curnode
        thissym = curnode.symbols.pop()
        if thissym.type == 'STRING':
            writestr = '\n;WRITES ' + thissym.name + writestr
            minilist = [OpNode('WRITES', '', '', thissym.name, '', '')] + minilist
        else:
            writestr = '\n;WRITE' + optype + ' ' + thissym.name + writestr
            minilist = [OpNode('WRITE' + optype, '', '', thissym.name, '', '')] + minilist
    irString += writestr
    opList += minilist
    pass


def p_basic_return_stmt(p):
    'return_stmt : RETURN expr SEMICOLON'
    pass


# Expressions List
def p_expressions_expr(p):
    '''expr : expr_prefix factor'''
    global irString
    global optype
    global opList
    if p[1]:
        nreg = nextReg()
        p[0] = nreg
        if p[1][-1] == '+':
            irString += '\n;ADD' + optype + ' ' + p[1][:-1] + " " + p[2] + nreg
            opList += [OpNode('ADD' + optype, p[1][:-1], p[2], nreg, '', '')]
        else:
            irString += '\n;SUB' + optype + ' ' + p[1][:-1] + " " + p[2] + nreg
            opList += [OpNode('SUB' + optype, p[1][:-1], p[2], nreg, '', '')]
    else:
        p[0] = p[2]

    pass


def p_expressions_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
    | empty'''
    global irString
    global  optype
    global opList
    if len(p.slice) > 2:
        if p[1]:
            nreg = nextReg()
            if p[1][-1] == '+':
                irString += '\n;ADD' + optype + ' ' + p[1][:-1] + " " + p[2] + nreg
                opList += [OpNode('ADD' + optype, p[1][:-1], p[2], nreg, '', '')]
                p[0] = nreg + p[3]
            else:
                irString += '\n;SUB' + optype + ' ' + p[1][:-1] + " " + p[2] + nreg
                opList += [OpNode('SUB' + optype, p[1][:-1], p[2], nreg, '', '')]
                p[0] = nreg + p[3]
        else:
            p[0] = p[2] + p[3]

    pass


def p_expressions_factor(p):
    'factor : factor_prefix postfix_expr'
    global irString
    global optype
    global opList
    if p[1]:
        nreg = nextReg()
        p[0] = nreg
        if p[1][-1] == "*":
            irString += '\n;MULT' + optype + ' ' + p[1][:-1] + " " + p[2] + nreg
            opList += [OpNode('MULT' + optype, p[1][:-1], p[2], nreg, '', '')]
        else:
            irString += '\n;DIV' + optype + ' ' + p[1][:-1] + " " + p[2] + nreg
            opList += [OpNode('DIV' + optype, p[1][:-1], p[2], nreg, '', '')]

    else:
        p[0] = p[2]

    pass


def p_expressions_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
    | empty'''
    if len(p.slice) > 2:
        if p[2]:
            p[0] = p[2] + p[3]
        else:
            p[0] = p[3]

    pass


def p_expressions_postfix_expr(p):
    '''postfix_expr : primary
    | call_expr'''
    p[0] = p[1]
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

    # Global variables
    global assignNode
    global idnames
    global irString
    global optype
    global opList

    # If float or int literal, store to register
    stype = p.slice[1].type
    if stype == 'INTLITERAL' or stype == 'FLOATLITERAL' :
        nreg = nextReg()
        irString += "\n;STOREI " + p[1] + nreg
        opList += [OpNode('STOREI', p[1], '', nreg, '', '')]
        p[0] = nreg
        if stype == 'INTLITERAL':
            optype = 'I'
        else:
            optype = 'F'
    elif(stype == 'id'):
        p[0] = p[1]
    elif(len(p.slice) == 4):
        p[0] = p[2]
    pass
    #primary

def p_expressions_addop(p):
    '''addop : PLUS
    | MINUS'''
    p[0] = p[1]
    pass


def p_expressions_mulop(p):
    '''mulop : MULTIPLY
    | DIVIDE'''
    p[0] = p[1]
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
        thisnode.name = "BLOCK " + str(blockCount)
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
    global irString
    global irlabel
    global opList

    # Add label to output string
    irString += '\n;LABEL label' + str(irlabel)
    opList += [OpNode('LABEL', '', '', '', '', 'label' + str(irlabel))]
    irlabel += 1

    # Increment scope and block count
    currentScope += 1
    blockCount += 1

    # Create new node
    thisnode = Node()
    thisnode.scopeLevel = currentScope
    thisnode.name = "BLOCK " + str(blockCount)
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

    # Make comparison
    operation = ""
    if (p.slice[1].type == 'EQUAL'):
        operation = "\n;EQI "
    elif(p.slice[1].type == 'NOTEQUAL'):
        operation = "\n;NEI"
    elif (p.slice[1].type == 'GREATER'):
        operation = "\n;GTI"
    elif (p.slice[1].type == 'GREATEQUAL'):
        operation = "\n;GEI"
    elif (p.slice[1].type == 'LESS'):
        operation = "\n;LTI"
    elif (p.slice[1].type == 'LESSEQUAL'):
        operation = "\n;LEI"


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

def nextReg():
    global regCounter
    temp = regCounter
    regCounter += 1
    return " $T" + str(temp)

# Print off symbol tables for scopes
def treeTraversal(node):

    global printstr

    # Check for duplicate symbols
    if(len(node.symbols) > 0):
        checkDuplicates(node)

    if(accepted):
        # Print root node information
        printinfo(node)

    # Traverse the rest of the tree and print off information
    for n in node.children:
        treeTraversal(n)


# Check for duplicates in symbol table
def checkDuplicates(node):

    # Define global variables
    global printstr
    global accepted

    # Check for any duplicates
    for i in range(0, len(node.symbols)):
        comparename = node.symbols[i].name
        for j in range(i + 1, len(node.symbols)):
            if(comparename == node.symbols[j].name):
                printstr = "DECLARATION ERROR " + comparename
                accepted = False
                return


# Print information for node
def printinfo(node):

    # Define  global variables
    global printstr

    # Print node name
    printstr = printstr + "Symbol table " + node.name + "\n"

    # Iterate through each symbol and print it off
    for s in node.symbols:

        # Print symbol name and type
        str = "name " + s.name + " type " + s.type

        # Only print symbol value if it exists
        if (s.value != ""):
            if(s.value == "\"\n\""):
                s.value = "\"\\n\""
            str = str + " value " + s.value
        printstr = printstr + str + "\n"
    printstr = printstr + "\n"

# Get input
#filename = sys.argv[1]
#f = open(filename,"r")
#data = f.read()
data = '''PROGRAM expr
BEGIN

	INT a,b,c,d;
	FLOAT x,y,z,t;
	STRING newline := "\n";

	FUNCTION VOID main()
	BEGIN
		WRITE (t, newline);
	END
END
'''

# Build parser and parse data
parser = yacc.yacc()
result = parser.parse(data)

# Traverse tree
treeTraversal(root)

# Remove trailing newlines and print out tables
printstr = printstr.rstrip()
#print(printstr)



print(convert())

# Print IR representation stuff
print("\n\n" + irString.replace('  ', ' ') + '\n;RET\n;tiny code')

