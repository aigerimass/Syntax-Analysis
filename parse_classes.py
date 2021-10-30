import copy

class Program:
    def __init__(self, arg):
        self.functions = arg
        self.dic_functions = dict()
        for func in self.functions:
            self.dic_functions[func.name] = func

    def show(self):
        for func in self.functions:
            func.show()
            print("--------")

    def arithmetic_parse(self):
        self.dic_functions["Main"].func_parse([], self.dic_functions)

    def __repr__(self):
        for func in self.functions:
            # print(func)
            func.print()
            print("------------")
        return ""


class Function:
    def __init__(self, name, args, body, line_count):
        self.name = name
        self.args = args
        self.body = body
        self.functions = dict()
        self.values = dict()
        self.bounds = []
        self.bounds.append(dict())
        self.line_number = [0]

    def print(self, god_bounds=None, god_line=None):
        self.line_number[0] = 0
        print(self.name, '(', end='')
        print(*self.args, sep='; ', end=') {\n')
        for n, v in self.bounds[0].items():
            print("#" + str(n) + " = " + str(v))
        self.line_number[0] += 1
        for op in self.body:
            op.print(self.bounds, self.line_number)
            print(';')
            for var in self.bounds[self.line_number[0]]:
                print("#" + var + " = ",
                      self.bounds[self.line_number[0]][var],
                      sep="", end=';\n')

            self.line_number[0] += 1
        print("};")
        return ""

    def show(self):
        print("Function Definition: [\nname = \"", self.name, "\",\nargs:", sep="", end=" ")
        for arg in self.args[:-1]:
            print("\"", arg, "\"", sep="", end=", ")
        if len(self.args) != 0:
            print(self.args[-1], end="")
        print("\nbody:")
        for op in self.body:
            op.show()
            print(";\n")
        print("]")

    def parse_expr(self, expr, line_number):
        expr_type = type(expr)
        if expr_type is Exp:
            return self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpWithoutOr:
            return self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpWithoutAnd:
            return self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpWithoutNot:
            return self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpWithoutCompare:
            return self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpWithoutUnaryMinus:
            return self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpMonomial:
            return self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpIndivisible:
            return self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpOr:
            return self.parse_expr(expr.arg1, line_number) or self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpAnd:
            return self.parse_expr(expr.arg1, line_number) and self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpNot:
            return not (self.parse_expr(expr.arg, line_number))
        elif expr_type is ExpEqual:
            return self.parse_expr(expr.arg1, line_number) == self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpGreater:
            return self.parse_expr(expr.arg1, line_number) > self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpGreaterEqual:
            return self.parse_expr(expr.arg1, line_number) >= self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpLess:
            return self.parse_expr(expr.arg1, line_number) < self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpLessEqual:
            return self.parse_expr(expr.arg1, line_number) <= self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpPlus:
            return self.parse_expr(expr.arg1, line_number) + self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpMinus:
            return self.parse_expr(expr.arg1, line_number) - self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpMultiply:
            return self.parse_expr(expr.arg1, line_number) * self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpDivision:
            return self.parse_expr(expr.arg1, line_number) // self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpUnaryMinus:
            return -self.parse_expr(expr.arg, line_number)
        elif expr_type is ExpPower:
            return self.parse_expr(expr.arg1, line_number) ** self.parse_expr(expr.arg2, line_number)
        elif expr_type is ExpUnit:
            unit_type = type(expr.arg)
            if unit_type is Variable:
                if expr.arg.name not in self.values:
                    print("ERROR: VARIABLE \"", expr.arg.name, "\" doesn't exist", sep='')
                    exit(1)
                return self.values[expr.arg.name]
            elif unit_type is Number:
                return int(expr.arg.arg)
            elif unit_type is StringLiteral:
                return str(expr.arg.arg)
            elif unit_type is ExpInBrackets:
                return self.parse_expr(expr.arg.arg, line_number)
            elif unit_type is OpFuncCall:
                if not (expr.arg.name in self.functions):
                    print("ERROR: the function", expr.arg.name, "has no declaration")
                    exit(1)
                return self.functions[expr.arg.name].func_parse(expr.arg.args, self.functions)
            else:
                print("ERROR: wrong EXPRESSION")
                exit(1)
        else:
            assert 0

    def body_parse(self, body):
        for op in body:
            self.bounds.append(copy.deepcopy(self.bounds[-1]))
            if type(op) is OpBinding:
                self.values[op.variable.name] = self.parse_expr(op.expr, self.line_number)
                if type(self.values[op.variable.name]) is int:
                    prev_values = [self.values[op.variable.name], self.values[op.variable.name]]
                    if op.variable.name in self.bounds[-1]:
                        prev_values = self.bounds[-1][op.variable.name]
                    up_bound = max(
                        prev_values[1],
                        self.values[op.variable.name])
                    down_bound = min(
                        prev_values[0],
                        self.values[op.variable.name])
                    self.bounds[-1][op.variable.name] = [down_bound, up_bound]
            elif type(op) is OpIf:
                b_before, v_before = self.bounds[-1].copy(), dict(self.values)
                return_if = self.body_parse(op.body)
                b_after_if, v_after_if = self.bounds[-1].copy(), dict(self.values)
                self.values = dict(v_before)
                self.bounds.append(copy.deepcopy(b_before))
                return_else = self.body_parse(op.body_else)
                b_after_else, v_after_else = dict(self.bounds[-1]), dict(self.values)
                self.values = dict(v_before)

                # for var in b_before:
                #     b_before[var][0] = min(b_after_if[var][0], b_after_else[var][0])
                #     b_before[var][1] = max(b_after_if[var][1], b_after_else[var][1])
                if self.parse_expr(op.condition, self.line_number[0]):
                    self.bounds.append(copy.deepcopy(b_after_if))
                    self.values = v_after_if
                    if return_if is not OpSkip:
                        return return_if
                else:
                    self.bounds.append(copy.deepcopy(b_after_else))
                    self.values = v_after_else
                    if return_else is not OpSkip:
                        return return_else
            elif type(op) is OpFuncCall:
                if op.name == "Write":
                    print(
                        self.parse_expr(op.args[0], self.line_number[0])
                    )
                elif op.name == "Read":
                    exit(1)
                elif not (op.name in self.functions):
                    print("ERROR: the function", op.name, "has no declaration")
                    exit(1)
                else:
                    self.functions[op.name].func_parse(op.args, self.functions)
            elif type(op) is OpWhile:
                while self.parse_expr(op.condition, self.line_number[0]):
                    x = self.body_parse(op.body)
                    if x is not OpSkip:
                        return x
            elif type(op) is OpFuncReturn:
                return self.parse_expr(op.expr, self.line_number[0])
            elif type(op) is OpSkip:
                continue
            else:
                assert 0
        return OpSkip

    def func_parse(self, args, all_functions):
        self.line_number[0] = 0
        self.functions = all_functions
        line_number = 0
        for (expr, var_name) in zip(args, self.args):
            self.values[var_name] = self.parse_expr(expr, line_number)
            if var_name not in self.bounds:
                self.bounds[line_number][var_name] = [self.values[var_name], self.values[var_name]]
            up_bound = max(self.bounds[line_number][var_name][1],
                           self.values[var_name])
            down_bound = min(self.bounds[line_number][var_name][0],
                             self.values[var_name])
            self.bounds[line_number][var_name] = [down_bound, up_bound]
        return self.body_parse(self.body)


class OpSkip:
    def __init__(self):
        pass

    def print(self, god_bounds, god_line):
        print("skip")

    def show(self):
        print("Skip()", end="")


class OpIf:
    def __init__(self, condition, body, body_else):
        self.condition = condition
        self.body = body
        self.body_else = body_else

    def print(self, god_bounds, god_line):
        print("if", ' (', end='')
        print(self.condition, end=') {\n')
        god_line[0] += 1
        for op in self.body:
            op.print(god_bounds, god_line)
            print(";")
            if type(op) is OpBinding and op.variable.name in god_bounds[god_line[0]]:
                print("#" + op.variable.name + " = ",
                      god_bounds[god_line[0]][op.variable.name],
                      sep="", end=';\n')
            god_line[0] += 1
        print("}", end="")
        god_line[0] += 1
        if self.body_else:
            print(" else {")
            for op in self.body_else:
                op.print(god_bounds, god_line)
                print(";")
                if type(op) is OpBinding and op.variable.name in god_bounds[god_line[0]]:
                    print("#" + op.variable.name + " = ",
                          god_bounds[god_line[0]][op.variable.name],
                          sep="", end=';\n')
                god_line[0] += 1
            print("}", end="")
        return ""

    def show(self):
        print(">If(")
        print("cond:")
        self.condition.show()
        print("\nbody:")
        for op in self.body:
            op.show()
            print(";")
        if self.body_else:
            print("else body:")
            for op in self.body:
                op.show()
                print(";")
        print(")", end="")


class OpWhile:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def print(self, god_bounds, god_line):
        print("while (", self.condition, ") {", sep="")
        # print(*self.body, sep=";\n", end=";\n")
        for op in self.body:
            op.print(god_bounds, god_line)
            if type(op) is OpBinding and op.variable.name in god_bounds:
                print("#" + op.variable.name + " = ",
                      god_bounds[god_line[0]][op.variable.name],
                      sep="", end=';\n')
            god_line[0] += 1
            print(";")
        print("}", end="")

    def show(self):
        print(">While(\ncond: ")
        self.condition.show()
        print("\nbody:")
        for op in self.body:
            op.show()
            print(";")
        print(")", end="")


class OpBinding:
    def __init__(self, variable, expr):
        self.variable = variable
        self.expr = expr

    def print(self, god_bounds=None, god_line=None):
        print(self.variable.name, "=", self.expr, end="")
        return ""

    def show(self):
        print(">Bind(", end="")
        self.variable.show()
        print(", ", end="")
        self.expr.show()
        print(")", end="")


class OpFuncCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def print(self, god_bounds=None, god_line=None):
        print(self.name, " (", sep="", end="")
        print(*self.args, sep=";", end=")")
        return ""

    def __repr__(self, god_bounds=None, god_line=None):
        print(self.name, " (", sep="", end="")
        print(*self.args, sep=";", end=")")
        return ""

    def show(self):
        print(">Call(name: \"", self.name, "\", args: ", end="", sep="")
        if not self.args:
            print(")", end="")
            return
        for arg in self.args[:-1]:
            arg.show()
            print(", ", end="")
        self.args[-1].show()
        print(")", end="")


class OpFuncReturn:
    def __init__(self, expr):
        self.expr = expr

    def print(self, god_bounds=None, god_line=None):
        print("return ", self.expr, sep="", end="")
        return ""

    def show(self):
        print(">Return(", end="")
        self.expr.show()
        print(")", end="")


class Exp:  # E
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class ExpOr:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "||", self.arg2, end="")
        return ""

    def show(self):
        print("Or(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpWithoutOr:  # W
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class ExpAnd:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "&&", self.arg2, end="")
        return ""

    def show(self):
        print("And(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpWithoutAnd:  # V
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class ExpNot:
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        print("Not(", end="")
        self.arg.show()
        print(")", end="")


class ExpWithoutNot:  # U
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class ExpEqual:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "==", self.arg2, end="")
        return ""

    def show(self):
        print("Eq(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpNotEqual:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "!=", self.arg2, end="")
        return ""

    def show(self):
        print("NotEq(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpLess:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "<", self.arg2, end="")
        return ""

    def show(self):
        print("Lt(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpLessEqual:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "<=", self.arg2, end="")
        return ""

    def show(self):
        print("Leq(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpGreater:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, ">", self.arg2, end="")
        return ""

    def show(self):
        print("Gt(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpGreaterEqual:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, ">=", self.arg2, end="")
        return ""

    def show(self):
        print("Geq(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpWithoutCompare:  # S
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class ExpPlus:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "+", self.arg2, end="")
        return ""

    def show(self):
        print("Plus(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpMinus:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "-", self.arg2, end="")
        return ""

    def show(self):
        print("Minus(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpMonomial:  # M without + and -
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class ExpMultiply:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "*", self.arg2, end="")
        return ""

    def show(self):
        print("Mult(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpDivision:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "//", self.arg2, end="")
        return ""

    def show(self):
        print("Div(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpIndivisible:  # T
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class ExpUnaryMinus:
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print("(-", self.arg, ")", sep='', end="")
        return ""

    def show(self):
        print("UnaryMinus(", end="")
        self.arg.show()
        print(")", end="")


class ExpWithoutUnaryMinus:  # P
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class ExpPower:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        print(self.arg1, "^^", self.arg2, end="")
        return ""

    def show(self):
        print("Pow(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpUnit:  # A
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        self.arg.show()


class Number:
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return self.arg

    def show(self):
        print(self.arg, end="")


class StringLiteral:
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print(self.arg, end="")
        return ""

    def show(self):
        print("String(", self.arg, ")", end="", sep="")


class ExpInBrackets:
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        print("(", self.arg, ")", sep="", end="")
        return ""

    def show(self):
        print("(", end="")
        self.arg.show()
        print(")", end="")


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        # print(self.name, end="")
        return self.name

    def show(self):
        print("Var \"", self.name, "\"", end="", sep="")
