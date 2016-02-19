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

# While statements

def p_whilestatements_while_stmt(p):
    'while_stmt : KEYWORDS ( cond ) decl stmt_list KEYWORDS'

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