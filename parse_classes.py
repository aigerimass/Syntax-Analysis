class Program:
    def __init__(self, arg):
        self.functions = arg


class Function:
    def __init__(self, name, args, body, ret_value):
        self.name = name
        self.args = args
        self.body = body
        self.ret_value = ret_value