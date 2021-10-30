import sys
import ply.yacc as yacc

from lex import tokens
from parse_classes import *


def p_program(p):
    '''program : list_of_functions main'''
    p[0] = Program(p[1] + [p[2]])


def p_list_of_functions(p):
    '''list_of_functions : func_init list_of_functions
                        |'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_main(p):
    '''main : MAIN ROUND_OPEN_BRACKET ROUND_CLOSED_BRACKET CURLY_OPEN_BRACKET list_of_op CURLY_CLOSED_BRACKET'''
    p[0] = Function(p[1], [], p[5], len(p[5]))


def p_func_init(p):
    '''func_init : FUNCTION ROUND_OPEN_BRACKET list_of_args ROUND_CLOSED_BRACKET CURLY_OPEN_BRACKET list_of_op CURLY_CLOSED_BRACKET'''
    p[0] = Function(p[1], p[3], p[6], len(p[6]))


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
    '''op_if : IF ROUND_OPEN_BRACKET expr ROUND_CLOSED_BRACKET CURLY_OPEN_BRACKET list_of_op CURLY_CLOSED_BRACKET ELSE CURLY_OPEN_BRACKET list_of_op CURLY_CLOSED_BRACKET
             | IF ROUND_OPEN_BRACKET expr ROUND_CLOSED_BRACKET CURLY_OPEN_BRACKET list_of_op CURLY_CLOSED_BRACKET'''
    if len(p) == 12:
        p[0] = OpIf(p[3], p[6], p[10])
    else:
        p[0] = OpIf(p[3], p[6], [])


def p_op_while(p):
    '''op_while : WHILE ROUND_OPEN_BRACKET expr ROUND_CLOSED_BRACKET CURLY_OPEN_BRACKET list_of_op CURLY_CLOSED_BRACKET'''
    p[0] = OpWhile(p[3], p[6])


def p_op_bind(p):
    '''op_bind : VARIABLE BINDING expr'''
    p[0] = OpBinding(Variable(p[1]), p[3])


def p_op_return(p):
    '''op_return : RETURN expr'''
    p[0] = OpFuncReturn(p[2])


def p_f_call(p):
    '''f_call : FUNCTION ROUND_OPEN_BRACKET list_of_args_call ROUND_CLOSED_BRACKET
              | READ ROUND_OPEN_BRACKET list_of_args_call ROUND_CLOSED_BRACKET
              | WRITE ROUND_OPEN_BRACKET list_of_args_call ROUND_CLOSED_BRACKET'''
    p[0] = OpFuncCall(p[1], p[3])


def p_list_of_args_call(p):
    '''list_of_args_call : expr SEMICOLON list_of_args_call
                   | expr
                   |'''
    p[0] = []
    if len(p) == 1:
        return
    p[0] += [p[1]]
    if len(p) == 4:
        p[0] += p[3]


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
    if len(p) == 2:
        p[0] = ExpMonomial(p[1])
    elif p[2] == "*":
        p[0] = ExpMonomial(ExpMultiply(p[1], p[3]))
    else:
        p[0] = ExpMonomial(ExpDivision(p[1], p[3]))


def p_expr_indivisible(p):
    '''expr_indivisible : ROUND_OPEN_BRACKET MINUS expr_positive ROUND_CLOSED_BRACKET
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
    '''expr_unit : expr_number
                 | expr_string
                 | expr_variable
                 | f_call
                 | ROUND_OPEN_BRACKET expr ROUND_CLOSED_BRACKET'''
    if len(p) == 4:
        p[0] = ExpUnit(ExpInBrackets(p[2]))
    else:
        p[0] = ExpUnit(p[1])


def p_expr_number(p):
    '''expr_number : NUMBER'''
    p[0] = Number(p[1])


def p_expr_string(p):
    '''expr_string : STRING'''
    p[0] = StringLiteral(p[1])


def p_expr_variable(p):
    '''expr_variable : VARIABLE'''
    p[0] = Variable(p[1])


def p_error(p):
    print("Syntax error", p)
    # exit(1) Разве здесь это нужно?


sys.stdout = open(sys.argv[1] + '.out', 'w')

print("----------SYNTAX-ANALYSIS----------")
parser = yacc.yacc()
s = open(sys.argv[1], 'r').read()

result = parser.parse(s)
result.show()
print("----------Run----------------------")
result.arithmetic_parse()
print("----------INTERVAL-ANALYSIS--------")
print(result)
