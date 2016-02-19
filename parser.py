import ply.yacc as yacc
from scanner import tokens
import sys

from Tools.scripts.treesync import raw_input

from scanner import tokens

# Program

def p_program_program(p):
    'program : KEYWORDS id KEYWORDS pgm_body KEYWORDS'

def p_program_idea(p):
    'id : IDENTIFIER'

def p_program_pgm_body(p):
    'pgm_body : func_declarations'

def p_program_decl(p):
    '''decl : string_decl decl
    | var_decl
    | empty'''

# Global String

def p_gstring_string_decl(p):
    'string_decl : KEYWORDS id := str'

def p_gstring_str(p):
    'str : STRINGLITERAL'

# Variables

def p_variables_var_decl(p):
    'var_decl : var_type id_list'

def p_variables_var_type(p):
    'var_type : KEYWORD'

def p_variables_any_type(p):
    '''any_type : var_type
    | KEYWORDS'''

def p_variables_id_list(p):
    'id_list : id id_tail'

def p_variables_id_tail(p):
    '''id_tail : id id_tail
    | empty'''

# Function parameter list

def p_fparams_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
    | empty'''

def p_fparams_param_decl(p):
    'param_decl : var_type id'

def p_fparams_param_decl_tail(p):
    '''param_decl_tail : param_decl param_decl_tail
    | empty'''

# Function declaration list

def p_fdecl_func_declarations(p):
    '''func_declarations : func_decl func_declarations
    | empty'''

def p_fdecl_func_decl(p):
    'func_decl : KEYWORDS any_type id (param_decl_list) KEYWORDS func_body KEYWORDS'

def p_fdecl_func_body(p):
    'func_body : decl stmt_list'

# Statement list

def p_statements_stmt_list(p):
    '''stmt_list : stmt stmt_list
    | empty'''

def p_statements_stmt(p):
    '''stmt : base_stmt
    | if_stmt
    | while_stmt'''

def p_statements_base_stmt(p):
    '''base_stmt : assign_stmt
    | read_stmt
    | write_stmt
    | return_stmt'''

##Basic bitch statements
def p_basic_assign_stmt(p):
   'assign_stmt: assign_expr ;'
   
def p_basic_assign_expr(p):
   'assign_expr: id := espr'
   
def p_basic_read_stmt(p):
   'read_stmt: KEYWORDS ( id_list );'
   
def p_basic_write_stmt(p):
   'write_stmt: KEYWORDS (id_list );'
   
def p_basic_return_stmt(p):
   'return_stmt: KEYWORDS expr ;'
   
   
# Expressions List	
	
def p_expressions_expr(p):
    'expr : expr_prefix factor'

def p_expressions_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
    | empty'''

def p_expressions_factor(p):
    'factor : factor_prefix postfix_expr'

def p_expressions_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
    | empty'''

def p_expressions_postfix_expr(p):
    '''postfix_expr : primary
    | call_expr'''

def p_expressions_call_expr(p):
    'call_expr : id ( expr_list )'

def p_expressions_expr_list(p):
    '''expr_list : expr expr_list_tail
    | empty'''

def p_expressions_expr_list_tail(p):
    '''expr_list_tail : , expr expr_list_tail
    | empty'''

def p_expressions_primary(p):
    '''primary : ( expr )
    | id
    | INTLITERAL
    | FLOATLITERAL'''

def p_expressions_addop(p):
    '''addop : +
    | -'''

def p_expressions_mulop(p):
    '''mulop : *
    | /'''	

##Complex Statemetns
def p_complex_if_stmt(p):
   'if_stmt: KEYWORDS ( cond ) decl stmt_list else_part KEYWORDS'
   
def p_complex_else_part(p):
   '''else_part: KEYWORDS decl stmt_list 
   | empty'''
   
def p_complex_cond(p):
   '''else_part: KEYWORDS decl stmt_list
   | empty'''
	
#Error handling

def p_error(p):
    print('Syntax error in input!')

# Build parser
parser = yacc.yacc()

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
