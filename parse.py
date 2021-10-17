import sys
import ply.yacc as yacc

from lex import tokens
from parse_classes import *


def p_program(p):
    '''program : list_of_functions main'''
    p[0] = Program(p[1] + p[2])


def p_list_of_functions(p):
    '''list_of_functions : func_init list_of_functions
                        |'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


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
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]


def p_operation(p):
    '''operation : op_skip
               | op_if
               | op_while
               | op_bind
               | op_return
               | f_call'''
    p[0] = p[1]


def p_op_skip(p):
    '''op_skip : SKIP'''
    p[0] = OpSkip()


def p_op_if(p):
    '''op_if : IF BRACKET expr BRACKET BRACKET list_of_op BRACKET ELSE BRACKET list_of_op BRACKET
            | IF BRACKET expr BRACKET BRACKET list_of_op BRACKET'''
    if len(p) == 12:
        p[0] = OpIf(p[3], p[6], p[10])
    else:
        p[0] = OpIf(p[3], p[6], [])


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
    p[0] = OpFuncCall(p[1], p[3])


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
    '''expr_without_not : expr_without_compare EQUAL expr_without_compare
                        | expr_without_compare NEQ expr_without_compare
                        | expr_without_compare GEQ expr_without_compare
                        | expr_without_compare LEQ expr_without_compare
                        | expr_without_compare GT expr_without_compare
                        | expr_without_compare LT expr_without_compare
                        | expr_without_compare'''
    if len(p) == 2:
        p[0] = ExpWithoutNot(p[1])
    elif p[2] == "==":
        p[0] = ExpWithoutNot(ExpEqual(p[1], p[3]))
    elif p[2] == "!=":
        p[0] = ExpWithoutNot(ExpNotEqual(p[1], p[3]))
    elif p[2] == ">=":
        p[0] = ExpWithoutNot(ExpGreaterEqual(p[1], p[3]))
    elif p[2] == "<=":
        p[0] = ExpWithoutNot(ExpLessEqual(p[1], p[3]))
    elif p[2] == ">":
        p[0] = ExpWithoutNot(ExpGreater(p[1], p[3]))
    elif p[2] == "<":
        p[0] = ExpWithoutNot(ExpLess(p[1], p[3]))


def p_expr_without_compare(p):
    '''expr_without_compare : expr_without_compare PLUS expr_monomial
                            | expr_without_compare MINUS expr_monomial
                            | expr_monomial'''
    if len(p) == 2:
        p[0] = ExpWithoutCompare(p[1])
    elif p[2] == "+":
        p[0] = ExpWithoutCompare(ExpPlus(p[1], p[3]))
    else:
        p[0] = ExpWithoutCompare(ExpMinus(p[1], p[3]))


def p_expr_monomial(p):
    '''expr_monomial : expr_monomial MUL expr_indivisible
                     | expr_monomial DIV expr_indivisible
                     | expr_indivisible'''


def p_expr_indivisible(p):
    '''expr_indivisible : BRACKET MINUS expr_positive BRACKET
                        | expr_positive'''
    if len(p) == 2:
        p[0] = ExpIndivisible(p[1])
    else:
        p[0] = ExpIndivisible(ExpUnaryMinus(p[3]))


def p_expr_positive(p):
    '''expr_positive : expr_unit POW expr_positive
                     | expr_unit'''
    if len(p) == 2:
        p[0] = ExpWithoutUnaryMinus(p[1])
    else:
        p[0] = ExpWithoutUnaryMinus(ExpPower(p[1], p[3]))


def p_expr_unit(p):
    '''expr_unit : NUMBER
                 | STRING
                 | VARIABLE
                 | f_call
                 | BRACKET expr BRACKET'''
    if len(p) == 4:
        p[0] = ExpUnit(ExpInBrackets(p[2]))
    elif type(p[1]) == int:
        p[0] = ExpUnit(Number(p[1]))
    elif type(p[1]) == OpFuncCall:
        p[0] = ExpUnit(p[1])
    elif p[1][0] == "\"":
        p[0] = ExpUnit(StringLiteral(p[1]))
    else:
        p[0] = Variable(p[1])


def p_error(p):
    print("Syntax error")


sys.stdout = open(sys.argv[1] + '.out', 'w')

parser = yacc.yacc()
s = open(sys.argv[1], 'r').read()

result = parser.parse(s)
# result.show()
