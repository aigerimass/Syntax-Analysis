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

    def parse_main(self):
        self.dic_functions["Main"].func_parse([], self.dic_functions)

    def anal(self):
        print("gachi ANALYSE:")
        for n, v in self.dic_functions["Main"].bounds.items():
            print(str(n) + " = " + str(v))
            print()

    def __repr__(self):
        for func in self.functions:
            print(func)
        return ""


class Function:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body
        self.functions = dict()
        self.values = dict()
        self.bounds = dict()

    def __repr__(self):
        print(self.name, '(', end='')
        print(*self.args, sep='; ', end=') {\n')
        for n, v in self.bounds.items():
            print("#" + str(n) + " = " + str(v))
        print(*self.body, sep=";\n", end=";\n")
        return "}"

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

    def parse_expr(self, expr):
        expr_type = type(expr)
        if expr_type is Exp:
            return self.parse_expr(expr.arg)
        elif expr_type is ExpWithoutOr:
            return self.parse_expr(expr.arg)
        elif expr_type is ExpWithoutAnd:
            return self.parse_expr(expr.arg)
        elif expr_type is ExpWithoutNot:
            return self.parse_expr(expr.arg)
        elif expr_type is ExpWithoutCompare:
            return self.parse_expr(expr.arg)
        elif expr_type is ExpWithoutUnaryMinus:
            return self.parse_expr(expr.arg)
        elif expr_type is ExpMonomial:
            return self.parse_expr(expr.arg)
        elif expr_type is ExpIndivisible:
            return self.parse_expr(expr.arg)
        elif expr_type is ExpOr:
            return self.parse_expr(expr.arg1) or self.parse_expr(expr.arg2)
        elif expr_type is ExpAnd:
            return self.parse_expr(expr.arg1) and self.parse_expr(expr.arg2)
        elif expr_type is ExpNot:
            return not (self.parse_expr(expr.arg))
        elif expr_type is ExpEqual:
            return self.parse_expr(expr.arg1) == self.parse_expr(expr.arg2)
        elif expr_type is ExpGreater:
            return self.parse_expr(expr.arg1) > self.parse_expr(expr.arg2)
        elif expr_type is ExpGreaterEqual:
            return self.parse_expr(expr.arg1) >= self.parse_expr(expr.arg2)
        elif expr_type is ExpLess:
            return self.parse_expr(expr.arg1) < self.parse_expr(expr.arg2)
        elif expr_type is ExpLessEqual:
            return self.parse_expr(expr.arg1) <= self.parse_expr(expr.arg2)
        elif expr_type is ExpPlus:
            return self.parse_expr(expr.arg1) + self.parse_expr(expr.arg2)
        elif expr_type is ExpMinus:
            return self.parse_expr(expr.arg1) - self.parse_expr(expr.arg2)
        elif expr_type is ExpMultiply:
            return self.parse_expr(expr.arg1) * self.parse_expr(expr.arg2)
        elif expr_type is ExpDivision:
            return self.parse_expr(expr.arg1) // self.parse_expr(expr.arg2)
        elif expr_type is ExpUnaryMinus:
            return -self.parse_expr(expr.arg)
        elif expr_type is ExpPower:
            return self.parse_expr(expr.arg1) ** self.parse_expr(expr.arg2)
        elif expr_type is ExpUnit:
            unit_type = type(expr.arg)
            if unit_type is Variable:
                return self.values[expr.arg.name]
            elif unit_type is Number:
                return int(expr.arg.arg)
            elif unit_type is StringLiteral:
                return str(expr.arg.arg)
        elif expr_type is OpFuncCall:
            return self.func_parse(expr.args, self.functions[expr.name])
        else:
            assert 0

    def body_parse(self, body):
        for op in body:
            if type(op) is OpBinding:
                self.values[op.variable.name] = self.parse_expr(op.expr)
                if type(self.values[op.variable.name]) is int:
                    if op.variable.name not in self.bounds:
                        self.bounds[op.variable.name] = [self.values[op.variable.name], self.values[op.variable.name]]
                    up_bound = max(self.bounds[op.variable.name][1],
                                   self.values[op.variable.name])
                    down_bound = min(self.bounds[op.variable.name][0],
                                     self.values[op.variable.name])
                    self.bounds[op.variable.name] = [down_bound, up_bound]
            elif type(op) is OpIf:
                if self.parse_expr(op.condition):
                    x = self.body_parse(op.body)
                    if type(x) is not OpSkip:
                        return x
                else:
                    x = self.body_parse(op.body_else)
                    if type(x) is not OpSkip:
                        return x
            elif type(op) is OpFuncCall:
                self.functions[op.name].func_parse(op.args, self.functions)
            elif type(op) is OpWhile:
                while self.parse_expr(op.condition):
                    x = self.body_parse(op.body_else)
                    if type(x) is not OpSkip:
                        return x
            elif type(op) is OpFuncReturn:
                return self.parse_expr(op.expr)
            elif type(op) is OpSkip:
                continue
            else:
                assert 0
        return OpSkip

    def func_parse(self, args, all_functions):
        self.functions = all_functions
        for (expr, var_name) in zip(args, self.args):
            self.values[var_name] = self.parse_expr(expr)
            if var_name not in self.bounds:
                self.bounds[var_name] = [self.values[var_name], self.values[var_name]]
            up_bound = max(self.bounds[var_name][1],
                           self.values[var_name])
            down_bound = min(self.bounds[var_name][0],
                             self.values[var_name])
            self.bounds[var_name] = [down_bound, up_bound]
        return self.body_parse(self.body)


class OpSkip:
    def __init__(self):
        pass

    def __repr__(self):
        return "skip"

    def show(self):
        print("Skip()", end="")


class OpIf:
    def __init__(self, condition, body, body_else):
        self.condition = condition
        self.body = body
        self.body_else = body_else

    def __repr__(self):
        print("if", ' (', end='')
        print(self.condition,end=') {\n')
        print(*self.body, sep=";\n", end=";\n")
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

    def __repr__(self):
        print("while (", self.condition, ") {", sep="")
        return "}"

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

    def __repr__(self):
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

    def __repr__(self):
        print(self.name, " (", sep="", end="")
        print(*self.args, sep=";", end=")")
        return ""

    def show(self):
        print(">Call(name: \"", self.name, "\", args: ", end="", sep="")
        if not self.args:
            print("()", end="")
            return
        for arg in self.args[:-1]:
            arg.show()
            print(", ", end="")
        self.args[-1].show()
        print(")", end="")


class OpFuncReturn:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
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
        # print(self.arg, end="")
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
        print(self.arg, end="")
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

# t = ExpWithoutOr(ExpPower(ExpPlus(Number(3), StringLiteral("abcd")), Variable("tru")))
# t.show()
# print()
# g = OpFuncCall("namefunc", [Variable("arg1"), Variable("arg2")])
# g.show()
# print()
# r = OpFuncReturn(t)
# r.show()
# print()
# w = OpWhile(t, [g, r])
# w.show()
# i = OpIf(t, [w], [g])
# i.show()

# t = Program([Function("Main", [], [OpBinding(Variable("x"), ExpMultiply(ExpUnit(Number(10)), ExpUnit(Number(2)))),
#                                    OpBinding(Variable("y"), ExpPlus(ExpUnit(Number(1)), ExpUnit(Number(2)))),
#                                    OpBinding(Variable("x"), ExpOr(ExpUnit(Number(1)), ExpUnit(Number(2)))),
#                                    OpBinding(Variable("x"), ExpPlus(ExpUnit(Number(1)), ExpUnit(Number(2)))),
#                                    OpBinding(Variable("y"), ExpPower(ExpUnit(Number(2)), ExpUnit(Variable('x')))),
#                                    OpBinding(Variable("x"), ExpDivision(ExpUnit(Number(100)), ExpUnit(Number(2)))),
#                                    OpBinding(Variable("t"), ExpDivision(ExpUnit(Number(200)), ExpUnit(Number(1)))),
#                                    OpIf(ExpGreater(ExpUnit(Variable("t")), ExpUnit(Number(1000))), [
#                                        OpBinding(Variable("t"), ExpUnit(Number(1000)))],
#                                         [
#                                             OpBinding(Variable("t"), ExpUnit(Number(1)))
#                                          ]),
#                                    ],
#                       )])
# t.parse_main()
# t.anal()
