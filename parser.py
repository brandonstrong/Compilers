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
functionEntered = False

# String that will be printed at end
printstr = ""

# variables for IR
irString = ';IR code\n'
irlabel = 1
regCounter = 1
optype = ''
opList = []
registerNums = 0

def newRegs():
    global registerNums

    registerName ="r" + str(registerNums)
    registerNums = registerNums + 1

    return registerName



def convert():
    global irString
    #assemble = [irString.replace(";", "") for clean in irString.split('\n') if irString.replace()]
    # myOp = OpNode()

    # Vars and Strs must precede all codes and labels in tiny assembly
    # The only ops on string constants is sys writes sid
    # strings can include \n for end-of-line

    myVars = []
    myStrs = {}
    varDict ={}
    tempDict = {}

    def checkVars():
        if thisOp.op1:
            i=10

    assembled = ""

    # new temporary numbers for Tiny ASS


    global opList
# need to change all temporary variables into registers.


# notation used for the operands:
# id      stands for the name of a memory location
# sid     stands for the name of a string constant
#         stands for an integer number
# target  stands for the name of a jump target
# $offset stands for a stack variable at address fp+offset
# reg     stands for a  register, named r0,r1,r2, or r3, case insensitive
# opmrl   stands for a memory id, stack variable, register or a number (literal),
#         the format for real is digit*[.digit*][E[+|-]digit*]
# opmr    stands for a memory id, stack variable, or a register


    for thisOp in opList:

        # check for variables and add to myVars

        # check for strings and add to my strings

        # check for register and if new one is needed

        tempReg = ""
        tempReg2 = ""
        thisOp.op1 = thisOp.op1.strip()
        thisOp.op2 = thisOp.op2.strip()
        thisOp.result = thisOp.result.strip()

        if thisOp.op1:
            if thisOp.op1[0] == '$':

                if thisOp.op1 not in tempDict:
                    tempReg = newRegs()
                    tempDict[thisOp.op1] = tempReg
                    thisOp.op1 = tempReg
                else:
                    thisOp.op1 = tempDict[thisOp.op1]

        if thisOp.op2:

            if thisOp.op2[0] == '$':

                if thisOp.op2 not in tempDict:
                    tempReg = newRegs()
                    tempDict[thisOp.op2] = tempReg
                    thisOp.op2 = tempReg
                else:
                    thisOp.op2 = tempDict[thisOp.op2]
        if thisOp.result:

            if thisOp.result[0] == '$':

                if thisOp.result not in tempDict:
                    tempReg = newRegs()
                    tempDict[thisOp.result] = tempReg
                    thisOp.result = tempReg
                else:
                    thisOp.result = tempDict[thisOp.result]

        # IR addi Op1 Op2 Result (int add)
        # Tiny addi opmrl reg, (integer addition), reg = reg + op1
        if thisOp.name == 'ADDI':
            assembled += "\nmove " + thisOp.op1 + " " + tempReg +"\naddi " + thisOp.op2 + " " + tempReg

        # IR addf Op1 Op2 Result (floating point add)
        # Tiny addr opmrl reg (real/float add), reg = reg + op1
        elif thisOp.name == 'ADDF':
            assembled += "\nmove " + thisOp.op1 + " " + tempReg + "\naddr " + thisOp.op2 + " " + tempReg

        # IR subi Op1 Op2  Result (int sub)
        # Tiny subi opmrl reg (int sub), reg = reg - op1
        elif thisOp.name == 'SUBI':
            #assembled += "\nmove " + thisOp.op2 + " " + tempReg + "\nsubi " + thisOp.op1 + " " + tempReg
            assembled += "\nmove " + thisOp.op1 + " " + tempReg + "\nsubi " + thisOp.op2 + " " + tempReg

        # IR subf Op1 Op2 Result (float subtract) Result = op1/op2
        # Tiny subr opmrl reg (real/float sub), reg = reg - op1
        elif thisOp.name == 'SUBF':
            #assembled += "\nmove " + thisOp.op2 + " " + tempReg + "\nsubr " + thisOp.op1 + " " + tempReg
            assembled += "\nmove " + thisOp.op1 + " " + tempReg + "\nsubf " + thisOp.op2 + " " + tempReg
        # IR multi op1 op2 result (int multiply)
        # Tiny muli opmrl reg (int mult), reg = reg * op1
        elif thisOp.name == 'MULTI':
            #assembled += "\nmove " + thisOp.op2 + " " + tempReg +"\nmuli " + tempReg + " " + thisOp.op1
            assembled += "\nmove " + thisOp.op1 + " " + tempReg + "\nmuli " + thisOp.op2 + " " + tempReg

        # IR multf op1 op2 result (float multiply)
        # Tiny mulr opmrl reg (real/float mult), reg = reg *op1
        elif thisOp.name == 'MULTF':
            assembled += "\nmove " + thisOp.op1 + " " + tempReg + "\nmulr " + thisOp.op2 + " " + tempReg

        # IR divi op1 op2 result (integer divide)
        # Tiny divi opmrl reg (int div), reg = reg / op1
        elif thisOp.name == 'DIVI':
            #assembled += "\nmove " + thisOp.op2 + " " + tempReg +"\ndivi " + tempReg + " " + thisOp.op1
            assembled += "\nmove " + thisOp.op1 + " " + tempReg + "\ndivi " + thisOp.op2 + " " + tempReg


        # IR divf op1 op2 result (float divide) Result = op1/op2
        # Tiny divr opmrl reg (real/float div) reg = reg / op1
        elif thisOp.name == 'DIVF':
            assembled += "\nmove " + thisOp.op1 + " " + tempReg +"\ndivr " + thisOp.op2 + " " + tempReg


        # IR storei op1 result (integer store, store op1 to result)
        # Tiny move opmrl opmr (only one operand can be a memory id
        #     or stack variable
        elif thisOp.name == 'STOREI':
            assembled += "\nmove " + thisOp.op1 + " " + thisOp.result

        # IR storef op1 result (FP Store)
        # Tiny move opmrl opmr (only one operand can be a memory id
        #     or stack variable
        elif thisOp.name == 'STOREF':
            assembled += "\nmove " + thisOp.op1 + " " + thisOp.result

        # IR gt op1 op2 label (if op1 > op2 goto label)
        # Tiny jgt target; jump if (op1 of the preceeding cmp was)
        # greater (than op2)
        elif thisOp.name == 'GT':
            assembled += "\ncmpi " + thisOp.op1 + " " + thisOp.op2 +\
                "\njgt" + thisOp.label + thisOp.string

        # IR ge op1 op2 LABEL (If OP1 >= OP2 Goto LABEL)
        # Tiny jge target             ; jump if greater of equal
        elif thisOp.name == 'GE':
            assembled += "\ncmpi " + thisOp.op1 + " " + thisOp.op2 +\
                "\njge" + thisOp.label + thisOp.string

        # IR lt op1 op2 LABEL (If OP1 <OP2 Goto LABEL)
        # Tiny jlt target             ; jump if less than
        elif thisOp.name == 'LT':
            assembled += "\ncmpi " + thisOp.op1 + " " + thisOp.op2 +\
                "\njlt" + thisOp.label + thisOp.string

        # IR le op1 op2 LABEL (If OP1 <= OP2 Goto LABEL
        # Tiny jle target             ; jump if less or equal
        elif thisOp.name == 'LE':
            assembled += "\ncmpi " + thisOp.op1 + " " + thisOp.op2 +\
                "\njle" + thisOp.label + thisOp.string

        # IR ne op1 op2 LABEL (If OP1 != OP2 Goto LABEL
        # Tiny jne target   ; jump if not equal
        elif thisOp.name == 'NE':
            assembled += "\ncmpi " + thisOp.op1 + " " + thisOp.op2 +\
                "\njne" + thisOp.label + thisOp.string

        # IR eq op1 op2 LABEL (If OP1 = OP2 Goto LABEL
        # Tiny jeq target             ; jump if equal
        elif thisOp.name == 'EQ':
            assembled += "\ncmpi " + thisOp.op1 + " " + thisOp.op2 +\
            "\njeq " + thisOp.label + thisOp.string

        # IR jump label (direct jump)
        # Tiny jmp target (unconditional jump)
        elif thisOp.name == 'JUMP':
            assembled += "\njmp " + thisOp.label + thisOp.string

        # IR label string (set a string label)
        # Tiny label target (a jump target)
        elif thisOp.name == 'LABEL':
            if thisOp.label:
                assembled += "\nlabel " + thisOp.label

        # IR readi result
        # Tiny sys readi opmr (a system call for reading
        #    an integer from input)
        elif thisOp.name == 'READI':
            assembled += "\nsys readi " + thisOp.result


        # IR readf result
        # Tiny sys readr opmr (system call for reading a real value)
        elif thisOp.name == 'READF':
            assembled += "\nsys readr " + thisOp.result

        # IR writei result
        # Tiny sys writei opmr (system call for outputting an integer)
        elif thisOp.name == 'WRITEI':
            assembled += "\nsys writei " + thisOp.result

        # IR writef result
        # Tiny sys writer opmr (system call for outputting a real)
        elif thisOp.name == 'WRITEF':
            assembled += "\nsys writer " + thisOp.result

        elif thisOp.name == 'STRINGY':
            if thisOp.string == '"\n"':
                assembled += repr(' "\n"').replace("'",'')
            else:
                assembled += '\n' + (thisOp.label + repr(thisOp.string).replace("'", '').replace('"', '')).replace("\n", '')

        elif thisOp.name == 'WRITES':

            if thisOp.result:

                    if thisOp.result not in myStrs:
                        # tempReg2 = newRegs()
                        myStrs[thisOp.result] = thisOp.string

            assembled += "\nsys writes " + thisOp.result
        # IR writes result
        # Tiny sys writes sid (system call for outputting a string constant

    # sys halt (system call to end the execution)
    #
    varString = ""


    assembled += "\nsys halt"
    return assembled





# Program
def p_program_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    pass


# Identifiers
def p_program_idea(p):
    'id : IDENTIFIER'
    global idnames
    global opList
    global functionEntered

    if not functionEntered :
        opList += [OpNode('STRINGY', '', '', '', 'var ', p[1])]

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
    global opList
    opList[-2].label = 'str '
    pass


def p_gstring_str(p):
    'str : STRINGLITERAL'

    # Declare global variables
    global curnode
    global idnames
    global optype
    global functionEntered
    global opList

    optype = 'S'
    # Create new symbol
    thissymbol = Symbol()
    thissymbol.name = idnames.pop()
    thissymbol.type = "STRING"
    thissymbol.value = p.slice[1].value

    # Add symbol to current node
    curnode.symbols = curnode.symbols + [thissymbol]

    if not functionEntered:
        opList += [OpNode('STRINGY', '', '', '', '', p[1])]

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
    global functionEntered
    functionEntered = True

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
    if len(p.slice) == 3:
        if p[1]:
            p[0] = p[1]
        else:
            p[0] = p[2]
    pass


def p_statements_stmt(p):
    '''stmt : base_stmt
    | if_stmt
    | while_stmt'''
    p[0] = p[1]
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
    writestr = ''
    minilist = []
    while i < reversPrevSize:
        i += 1
        # Consume symbol from curnode
        thissym = curnode.symbols.pop()
        if thissym.type == 'STRING':
            writestr = '\n;READS ' + thissym.name + writestr
            minilist = [OpNode('READS', '', '', thissym.name, '', thissym.value)] + minilist
        else:
            writestr = '\n;READ' + optype + ' ' + thissym.name + writestr
            minilist = [OpNode('READ' + optype, '', '', thissym.name, '', '')] + minilist
    irString += writestr
    opList += minilist
    pass


def p_basic_write_stmt(p):
    'write_stmt : WRITE LPAREN id_list RPAREN SEMICOLON'

    # Declare global variable
    global curnode
    global reversPrevSize
    global irString
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
            minilist = [OpNode('WRITES', '', '', thissym.name, '', thissym.value)] + minilist
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
   global irString
   global opList

   irString += '\n;LABEL ' + p[3]
   opList += [OpNode('LABEL', '', '', '', p[3], '')]
   p[0] = p[3]
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
        global irlabel
        global opList
        global irString

        # Add label to output string
        irString += '\n;JUMP ' + 'label' + str(irlabel)
        opList += [OpNode('JUMP', '', '', '', 'label' + str(irlabel), '')]
        p[0] = 'JUMP' + str(irlabel)
        irlabel += 1

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
    global irlabel
    global opList
    global irString

    # Add label to output string
    irString += ";\n" + p[2] + ' ' + p[1] + ' ' + p[3] + ' label' + str(irlabel)
    opList += [OpNode(";\n" + p[2], p[1], p[3], '', '', 'label' + str(irlabel))]
    p[0] = 'label' + str(irlabel)
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

    global optype

    # Make comparison
    operation = ""
    if (p.slice[1].type == 'EQUAL'):
        operation = ";EQ" + optype
    elif(p.slice[1].type == 'NOTEQUAL'):
        operation = ";NE" + optype
    elif (p.slice[1].type == 'GREATER'):
        operation = ";GT" + optype
    elif (p.slice[1].type == 'GREATEQUAL'):
        operation = ";GE" + optype
    elif (p.slice[1].type == 'LESS'):
        operation = ";LT" + optype
    elif (p.slice[1].type == 'LESSEQUAL'):
        operation = ";LE" + optype

    p[0] = operation
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
data = '''PROGRAM p
BEGIN

	INT a,b,c;

	FUNCTION VOID main()
	BEGIN
		a := 20;
		b := 30;
		c := 40;

		c := c + a*b + (a*b+c)/a + 20;
		b := b*b + a;
		a := (b*a)/a;

		WRITE (c);
		WRITE (b);
		WRITE (a);

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

# Print IR representation stuff
print(irString.replace('  ', ' ') + '\n;RET\n;tiny code')

print(convert())



