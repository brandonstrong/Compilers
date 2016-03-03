##########################################
#  CSCI-468 Compiler
#  Group 0 - Brandon Strong, Sawyer Payne,
#  and Matthew Gannon
#  Step 2 - Create a parser which will
#  verify tokens made from the scanner,
#  and check them against grammar of the
#  Little Language.
#
##########################################



import ply.yacc as yacc
from scanner import tokens
import sys
from scanner import tokens

# Global String
accepted = True


# ---- Program ----
def p_program_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    pass


# Identifier
def p_program_idea(p):
    'id : IDENTIFIER'
    pass


# Program body
def p_program_pgm_body(p):
    'pgm_body : decl func_declarations'
    pass


# Program Declaration
def p_program_decl(p):
    '''decl : string_decl decl
    | var_decl decl
    | empty'''
    pass

# ---- String ----
def p_gstring_string_decl(p):
    '''string_decl : STRING id ASSIGN str SEMICOLON'''
    pass


# String Literal
def p_gstring_str(p):
    'str : STRINGLITERAL'
    pass


# ----Variables----

def p_variables_var_decl(p):
    'var_decl : var_type id_list SEMICOLON'
    pass


# Variable Float
def p_variables_var_type(p):
    '''var_type : FLOAT
    | INT'''
    pass


# Variable
def p_variables_any_type(p):
    '''any_type : var_type
    | VOID'''
    pass


# Variable Identifier list
def p_variables_id_list(p):
    '''id_list : id id_tail'''
    pass


# Variable Identifier tail
def p_variables_id_tail(p):
    '''id_tail : COMMA id id_tail
    | empty'''
    pass


# Function parameter list
def p_fparams_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
    | empty'''
    pass


# Function Parameter declaration
def p_fparams_param_decl(p):
    'param_decl : var_type id'
    pass


# Function Parameter declaration tail
def p_fparams_param_decl_tail(p):
    '''param_decl_tail : COMMA param_decl param_decl_tail
    | empty'''
    pass


# Function declaration list
def p_fdecl_func_declarations(p):
    '''func_declarations : func_decl func_declarations
    | empty'''
    pass


# Function declaration
def p_fdecl_func_decl(p):
    'func_decl : FUNCTION any_type id LPAREN param_decl_list RPAREN BEGIN func_body END'
    pass


# Function declaration body
def p_fdecl_func_body(p):
    'func_body : decl stmt_list'
    pass


# Statement list
def p_statements_stmt_list(p):
    '''stmt_list : stmt stmt_list
    | empty'''
    pass


# Statement
def p_statements_stmt(p):
    '''stmt : base_stmt
    | if_stmt
    | while_stmt'''
    pass


# Statements
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


# Assignment expression
def p_basic_assign_expr(p):
    'assign_expr : id ASSIGN expr'
    pass


# Read Statements
def p_basic_read_stmt(p):
    'read_stmt : READ LPAREN id_list RPAREN SEMICOLON'
    pass


# Write Statements
def p_basic_write_stmt(p):
    'write_stmt : WRITE LPAREN id_list RPAREN SEMICOLON'
    pass


# Return Statement
def p_basic_return_stmt(p):
    'return_stmt : RETURN expr SEMICOLON'
    pass


# Expressions
def p_expressions_expr(p):
    '''expr : expr_prefix factor'''
    pass


# Expression Prefix
def p_expressions_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
    | empty'''
    pass


# Expression factor
def p_expressions_factor(p):
    'factor : factor_prefix postfix_expr'
    pass


# Expression factor prefix
def p_expressions_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
    | empty'''
    pass


# Expression Postfix
def p_expressions_postfix_expr(p):
    '''postfix_expr : primary
    | call_expr'''
    pass


# Expression call
def p_expressions_call_expr(p):
    'call_expr : id LPAREN expr_list RPAREN'
    pass


# Expression list
def p_expressions_expr_list(p):
    '''expr_list : expr expr_list_tail
    | empty'''
    pass


# Expression list tail
def p_expressions_expr_list_tail(p):
    '''expr_list_tail : COMMA expr expr_list_tail
    | empty'''
    pass


# Expression Primary
def p_expressions_primary(p):
    '''primary : LPAREN expr RPAREN
    | id
    | INTLITERAL
    | FLOATLITERAL'''
    pass


# Expression add operation
def p_expressions_addop(p):
    '''addop : PLUS
    | MINUS'''
    pass


# Expression multiply
def p_expressions_mulop(p):
    '''mulop : MULTIPLY
    | DIVIDE'''
    pass


# Complex If Statement
def p_complex_if_stmt(p):
    'if_stmt : IF LPAREN cond RPAREN decl stmt_list else_part ENDIF'
    pass


# Complex Else Statement
def p_complex_else_part(p):
    '''else_part : ELSE decl stmt_list
    | empty'''
    pass


# Complex Condition
def p_complex_cond(p):
    '''cond : expr compop expr'''
    pass


# Complex condition operation
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


# Get input
filename = sys.argv[1]
f = open(filename,"r")
data = f.read()

# Build parser
parser = yacc.yacc()

result = parser.parse(data)
if(accepted):
    print("Accepted")
else:
    print("Not accepted")

