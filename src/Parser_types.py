class Statement:
    def __repr__(self):
        return "Statement()"

class Expression:
    def __repr__(self):
        return "Expression()"

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class ReturnStatement(Statement):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ReturnStatement({self.value})"
    

class NumberLiteral(Expression):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"NumberLiteral({self.type}, {self.value})"

class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral({self.value})"
    
class BooleanLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"BooleanLiteral({self.value})"

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

class FunctionDeclaration(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"FunctionDeclaration({self.name}, {self.parameters}, {self.body})"

class FunctionCall(Expression):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.arguments})"

class Assignment(Statement):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def __repr__(self):
        return f"Assignment({self.variable}, {self.value})"

class BinaryOperation(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOperation({self.left}, {self.op}, {self.right})"

class ComparisonOperation(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"ComparisonOperation({self.left}, {self.op}, {self.right})"

class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Literal({self.value})"

class UnaryOperation(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOperation({self.op}, {self.operand})"

class VariableDeclaration(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VariableDeclaration({self.name}, {self.value})"

class IfStatement(Statement):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.if_body}, {self.else_body})"

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement({self.condition}, {self.body})"
