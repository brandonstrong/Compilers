import ply.yacc as yacc
from scanner import tokens
import sys

from Tools.scripts.treesync import raw_input

from scanner import tokens


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