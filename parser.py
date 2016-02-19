import ply.yacc as yacc
from scanner import tokens
import sys

from Tools.scripts.treesync import raw_input

from scanner import tokens

def p_program_program(p):
    'program : PROGRAM id BEGIN pgm_body END'

def p_program_id(p):
    'id : IDENTIFIER'

def p_program_pgm_body(p):
    'decl : func_declarations'

def p_program_decl(p):
    '''decl : string_decl decl
    | var_decl
    | empty'''

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