import ply.yacc as yacc
from scanner import tokens
import sys

from Tools.scripts.treesync import raw_input

from scanner import tokens

# Program

def p_program_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    pass

def p_program_idea(p):
    'id : IDENTIFIER'
    pass

def p_program_pgm_body(p):
    'pgm_body : decl func_declarations'
    pass

def p_program_decl(p):
    '''decl : string_decl decl
    | var_decl
    | empty'''
    pass

# Global String

def p_gstring_string_decl(p):
    '''string_decl : STRING id OPERATORS str'''
    pass

def p_gstring_str(p):
    'str : STRINGLITERAL'
    pass

# Variables

def p_variables_var_decl(p):
    'var_decl : var_type id_list'
    pass

def p_variables_var_type(p):
    '''var_type : FLOAT
    | INT'''
    pass

def p_variables_any_type(p):
    '''any_type : var_type
    | VOID'''
    pass

def p_variables_id_list(p):
    '''id_list : id id_tail'''
    pass

def p_variables_id_tail(p):
    '''id_tail : OPERATORS id id_tail
    | empty'''
    pass

# Function parameter list

def p_fparams_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
    | empty'''
    pass

def p_fparams_param_decl(p):
    'param_decl : var_type id'
    pass

def p_fparams_param_decl_tail(p):
    '''param_decl_tail : param_decl param_decl_tail
    | empty'''
    pass

# Function declaration list

def p_fdecl_func_declarations(p):
    '''func_declarations : func_decl func_declarations
    | empty'''
    pass

def p_fdecl_func_decl(p):
    'func_decl : FUNCTION any_type id OPERATORS param_decl_list OPERATORS BEGIN func_body END'
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
   'assign_stmt : assign_expr'
   pass

def p_basic_assign_expr(p):
   'assign_expr : id OPERATORS expr'
   pass

def p_basic_read_stmt(p):
   'read_stmt : READ OPERATORS id_list OPERATORS'
   pass

def p_basic_write_stmt(p):
   'write_stmt : WRITE OPERATORS id_list OPERATORS'
   pass

def p_basic_return_stmt(p):
   'return_stmt : RETURN expr '
   pass


# Expressions List

def p_expressions_expr(p):
    'expr : expr_prefix factor'
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
    'call_expr : id OPERATORS expr_list OPERATORS'
    pass

def p_expressions_expr_list(p):
    '''expr_list : expr expr_list_tail
    | empty'''
    pass

def p_expressions_expr_list_tail(p):
    '''expr_list_tail : OPERATORS OPERATORS expr expr_list_tail
    | empty'''
    pass

def p_expressions_primary(p):
    '''primary : OPERATORS expr OPERATORS
    | id
    | INTLITERAL
    | FLOATLITERAL'''
    pass

def p_expressions_addop(p):
    '''addop : OPERATORS OPERATORS
    | OPERATORS'''
    pass

def p_expressions_mulop(p):
    '''mulop : OPERATORS OPERATORS
    | OPERATORS'''
    pass

# Complex Statemetns
def p_complex_if_stmt(p):
   'if_stmt : IF OPERATORS cond OPERATORS decl stmt_list else_part ENDIF'
   pass

def p_complex_else_part(p):
   '''else_part : ELSE decl stmt_list
   | empty'''
   pass

def p_complex_cond(p):
   '''cond : expr compop expr'''
   pass

def p_complex_compop(p):
    '''compop : OPERATORS'''
    pass
# While statement

def p_whilestatement_while_stmt(p):
    'while_stmt : WHILE OPERATORS cond OPERATORS decl stmt_list ENDWHILE'
    pass

# Empty

def p_empty(p):
    'empty :'
    pass

# Error handling

def p_error(p):
    print(p)
    print('Syntax error in input!')

data = '''
PROGRAM test
BEGIN
FUNCTION VOID funk (FLOAT s)
BEGIN
STRING s = "fuck"
INT x = asdf
END
END
'''

# Build parser
parser = yacc.yacc()

print("\nPARSER OUTPUT:\n");

result = parser.parse(data)
print(result)

print("\nGive customized input:")
while False:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
