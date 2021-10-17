import sys
import ply.yacc as yacc
import parse_classes

from lex import tokens
from parse_classes import *


def p_program(p):
    '''program : list_of_functions main'''
    p[0] = Program(p[1] + p[2])


def p_list_of_functions(p):
    '''list_of_functions : func_init list_of_functions
                        |'''
    p[0] = [p[1]] + p[2]


def p_main(p):
    '''main : MAIN BRACKET BRACKET BRACKET list_of_op BRACKET'''
    p[0] = Function(p[1], [], p[5])


def p_func_init(p):
    '''func_init : FUNCTION BRACKET list_of_args BRACKET BRACKET list_of_op BRACKET'''
    p[0] = Function(p[1], p[3], p[6])


def p_list_of_args(p):
    '''list_of_args : VARIABLE SEMICOLON list_of_args
                   | VARIABLE
                   |'''
    p[0] = []
    if len(p) == 1:
        return
    p[0] += [p[1]]
    if len(p) == 4:
        p[0] += p[3]


def p_list_of_op(p):
    '''list_of_op : operation SEMICOLON list_of_op
                 |'''
    p[0] = []
    if len(p) == 1:
        return
    p[0] += p[1]


def p_operation(p):
    '''operation : op_skip
               | op_if
               | op_while
               | op_bind
               | op_return
               | f_call'''
    p[0] = p[1]


def p_op_skip(p):
    '''skip: SKIP'''
    p[0] = OpSkip()


def p_op_if(p):
    '''op_if : IF BRACKET expr BRACKET BRACKET list_of_op BRACKET ELSE BRACKET list_of_op BRACKET
            | IF BRACKET expr BRACKET BRACKET list_of_op BRACKET'''
    if len(p) == 12:
        p[0] = OpIf(p[3], p[6], p[10])
    else:
        p[0] = OpIf(p[3], p[6])


def p_op_while(p):
    '''op_while : WHILE BRACKET expr BRACKET BRACKET list_of_op BRACKET'''
    p[0] = OpWhile(p[3], p[6])


def p_op_bind(p):
    '''op_bind : VARIABLE BINDING expr'''
    p[0] = OpBinding(p[1], p[3])


def p_op_return(p):
    '''op_return : RETURN expr'''
    p[0] = OpFuncReturn(p[2])


def p_f_call(p):
    '''f_call : FUNCTION BRACKET list_of_args BRACKET'''


def p_expr(p):
    '''expr : expr_without_or OR expr
           | expr_without_or'''
    if len(p) == 2:
        p[0] = Exp(p[1])
    else:
        p[0] = Exp(ExpOr(p[1], p[3]))


def p_expr_without_or(p):
    '''expr_without_or : expr_without_and AND expr_without_or
                       | expr_without_and'''
    if len(p) == 2:
        p[0] = ExpWithoutOr(p[1])
    else:
        p[0] = ExpWithoutOr(ExpAnd(p[1], p[3]))


def p_expr_without_and(p):
    '''expr_without_and : NOT expr_without_not
                        | expr_without_not'''
    if len(p) == 2:
        p[0] = ExpWithoutAnd(p[1])
    else:
        p[0] = ExpWithoutAnd(ExpNot(p[2]))


def p_expr_without_not(p):
    '''expr_without_not : expr_without_compare EQUAL expr_without_compare'''

