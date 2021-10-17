class Program:
    def __init__(self, arg):
        self.functions = arg
        self.dic_functions = dict()
        for f in self.functions:
            self.dic_functions[f.name] = f

    def parse_main(self):
        self.dic_functions["Main"].func_parse([], self.dic_functions)

    def anal(self):
        for v in self.dic_functions["Main"].values:
            v.show()
            print()


class Function:
    def __init__(self, name, args, body, ret_value):
        self.name = name
        self.args = args
        self.body = body
        self.ret_value = ret_value
        self.functions = dict()
        self.values = dict()
        self.bounds = dict()

    def parse_expr(self, expr):
        expr_type = type(expr)
        if expr_type is ExpOr:
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
            return self.parse_expr(expr.arg1) / self.parse_expr(expr.arg2)
        elif expr_type is ExpUnaryMinus:
            return -self.parse_expr(expr.arg)
        elif expr_type is ExpPower:
            return self.parse_expr(expr.arg1) ^ self.parse_expr(expr.arg2)
        elif expr_type is ExpUnit:
            unit_type = type(expr.arg)
            if unit_type is Variable:
                return self.values[expr.arg.name]
            elif unit_type is Number:
                return expr.arg.arg
            elif unit_type is StringLiteral:
                return expr.arg.arg
        elif expr_type is OpFuncCall:
            return self.func_parse(expr.args, self.functions[expr.name])
        else:
            assert 0

    def body_parse(self, body):
        for op in body:
            if type(op) is OpBinding:
                self.values[op.variable.name] = self.parse_expr(op.expr)
                if type(self.values[op.variable.name]) is int:
                    up_bound = max(self.bounds.get(op.variable.name,
                                                   [self.values[op.variable.name], self.values[op.variable.name]])[1],
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
                self.func_parse(op.args, self.functions[op.name])
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
        for arg in args:
            self.values[self.args.name] = arg
        return self.body_parse(self.body)


class OpSkip:
    def __init__(self):
        pass


class OpIf:
    def __init__(self, condition, body, body_else):
        self.condition = condition
        self.body = body
        self.body_else = body_else

    def show(self):
        print("\nIf(")
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

    def show(self):
        print("While(\ncond: ")
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

    def show(self):
        print("Bind(", end="")
        print("Bind(", end="")
        self.variable.show()
        print(", ", end="")
        self.expr.show()
        print(")", end="")


class OpFuncCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def show(self):
        print("Call(name: \"", self.name, "\", args: ", end="", sep="")
        for arg in self.args[:-1]:
            arg.show()
            print(", ", end="")
        self.args[-1].show()
        print(")", end="")


class OpFuncReturn:
    def __init__(self, expr):
        self.expr = expr

    def show(self):
        print("Return(", end="")
        self.expr.show()
        print(")", end="")


class Exp:  # E
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        self.arg.show()


class ExpOr:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def show(self):
        print("Or(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpWithoutOr:  # W
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        self.arg.show()


class ExpAnd:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def show(self):
        print("And(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpWithoutAnd:  # V
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        self.arg.show()


class ExpNot:
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        print("Not(", end="")
        self.arg.show()
        print(")", end="")


class ExpWithoutNot:  # U
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        self.arg.show()


class ExpEqual:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

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

    def show(self):
        print("Geq(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpWithoutCompare:  # S
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        self.arg.show()


class ExpPlus:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

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


class ExpMonomial:  # M without + and -
    def __init__(self, arg):
        self.arg = arg


class ExpMultiply:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2


class ExpDivision:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def show(self):
        print("Div(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpIndivisible:  # T
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        self.arg.show()


class ExpUnaryMinus:
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        print("UnaryMinus(", end="")
        self.arg.show()
        print(")", end="")


class ExpWithoutUnaryMinus:  # P
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        self.arg.show()


class ExpPower:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def show(self):
        print("Pow(", end="")
        self.arg1.show()
        print(", ", end="")
        self.arg2.show()
        print(")", end="")


class ExpUnit:  # A
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        self.arg.show()


class Number:
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        print(self.arg, end="")


class StringLiteral:
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        print("\"", self.arg, "\"", end="", sep="")


class ExpInBrackets:
    def __init__(self, arg):
        self.arg = arg

    def show(self):
        print("(", end="")
        self.arg.show()
        print(")", end="")


class Variable:
    def __init__(self, name):
        self.name = name

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

t = Program([Function("Main", [], [OpBinding(Variable("x"), ExpPlus(ExpUnit(Number(1)), ExpUnit(Number(2))))], [])])
t.parse_main()
t.anal()