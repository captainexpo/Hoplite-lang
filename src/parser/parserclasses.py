
class Statement:
    kind: str = "statement"
    pass
class Expression:
    kind: str = "expression"
    pass

class DataType:
    pass

class FunctionDeclaration(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class FunctionCall(Statement):
    def __init__(self,name,arguments):
        self.name = name
        self.arguments = arguments

class VariableDeclaration(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Assignment(Statement):
    def __init__(self, name, value):
        self.name = name

class ReturnStatement(Statement):
    def __init__(self, value):
        self.value = value

class IfStatement(Statement):
    def __init__(self,condition,if_body,else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class WhileStatement(Statement):
    def __init__(self,condition,body):
        self.condition = condition
        self.body = body

class ComparisonOperation(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class BinaryOperation(Exception):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NumberType(DataType):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class StringType(DataType):
    def __init__(self,value):
        self.value = value

class BoolType(DataType):
    def __init__(self,value):
        self.value = value

class Variable:
    def __init__(self,name):
        self.name = name