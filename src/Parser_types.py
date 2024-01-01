# Updated class definitions with swapped AsLiteral and __repr__ methods

class Statement:
    def AsLiteral(self):
        return "Statement()"
    
    def __repr__(self):
        return ''

class Expression:
    def AsLiteral(self):
        return "Expression()"
    def __repr__(self):
        return ''
    
class DataType:
    def __init__(self, name, methods, value):
        self.name = name
        self.methods = methods
        self.value = value

    def add(self, other): raise Exception(f"Cannot add {self} and {other}")
    def subtract(self, other):raise Exception(f"Cannot sub {self} and {other}")
    def multiply(self, other):raise Exception(f"Cannot mul {self} and {other}")
    def divide(self, other):raise Exception(f"Cannot div {self} and {other}")
    def modulo(self, other):raise Exception(f"Cannot mod {self} and {other}")
    def power(self, other):raise Exception(f"Cannot pow {self} and {other}")
    def unary_not(self):raise Exception(f"Cannot perform !{self}")
    def unary_minus(self):raise Exception(f"Cannot perform -{self}")
    def is_equal(self, other):raise Exception(f"Cannot compare {self} and {other}")
    def is_not_equal(self, other):raise Exception(f"Cannot compare {self} and {other}")
    def is_less_than(self, other):raise Exception(f"Cannot compare {self} and {other}")
    def is_less_than_or_equal(self, other):raise Exception(f"Cannot compare {self} and {other}")
    def is_greater_than(self, other):raise Exception(f"Cannot compare {self} and {other}")
    def is_greater_than_or_equal(self, other):raise Exception(f"Cannot compare {self} and {other}")

    def AsLiteral(self):
        return f"DataType({self.name}, {self.methods}, {self.value})"

    def __repr__(self):
        return self.value

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def AsLiteral(self):
        return f"Block({self.statements})"

    def __repr__(self):
        return ''

class ReturnStatement(Statement):
    def __init__(self, value):
        self.value = value

    def AsLiteral(self):
        return f"ReturnStatement({self.value})"

    def __repr__(self):
        return ''
    

class NumberLiteral(DataType):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def AsLiteral(self):
        return f"NumberLiteral({self.type}, {self.value})"
    def add(self, other):
        return NumberLiteral(self.type, self.value + other.value)
    def subtract(self, other):
        return NumberLiteral(self.type, self.value - other.value)
    def multiply(self, other):
        return NumberLiteral(self.type, self.value * other.value)
    def divide(self, other):
        return NumberLiteral(self.type, self.value / other.value)
    def modulo(self, other):
        return NumberLiteral(self.type, self.value % other.value)
    def power(self, other):
        return NumberLiteral(self.type, self.value ** other.value)
    def __repr__(self):
        return str(self.value)
    def unary_minus(self):
        return NumberLiteral(self.type, -self.value)

class MethodCall(Expression):
    def __init__(self, variable, method_name, arguments):
        self.variable = variable
        self.method = method_name
        self.arguments = arguments

    def AsLiteral(self):
        arguments_str = ", ".join([str(arg) for arg in self.arguments])
        return f"MethodCall({self.variable}, {self.method}, [{arguments_str}])"

    def __repr__(self):
        return ''

class StringLiteral(DataType):
    def __init__(self, value):
        self.value = value

    def AsLiteral(self):
        return f"StringLiteral({self.value})"
    def add(self, other):
        if isinstance(other, StringLiteral):
            return StringLiteral(self.value + other.value)
        raise Exception(f"Cannot add \"{self}\" and {other}")
    def multiply(self, other):
        if isinstance(other, NumberLiteral):
            return StringLiteral(self.value * other.value)
        raise Exception(f"Cannot multiply \"{self}\" and {other}")
    def __repr__(self):
        return self.value

class ArrayLiteral(DataType):
    def __init__(self, elements):
        self.elements = elements
        self.methods = {
            "append": lambda item: self.append(item),
            "pop": lambda i: self.elements.pop(),
            "at": lambda index: self.elements[index[0].value],
        }
    def append(self, item):
        for i in item:
            self.elements.append(i)
    def AsLiteral(self):
        return f"ArrayLiteral({self.elements})"
    
    def __repr__(self):
        output = "["
        for i in self.elements:
            output += f"{i}, "
        output = output[:-2]
        output += "]"
        return output

class BooleanLiteral(DataType):
    def __init__(self, value):
        self.value = value == "true"
    def AsLiteral(self):
        return f"BooleanLiteral({self.value})"
    def unary_not(self) -> 'BooleanLiteral':
        print("VASEAWEAWEAWE",self.value, not self.value)
        return BooleanLiteral(self.value == False)
    def is_equal(self, other):
        if isinstance(other, BooleanLiteral):
            return BooleanLiteral(self.value == other.value)
        else:
            return BooleanLiteral(False)
    def is_not_equal(self, other):
        if isinstance(other, BooleanLiteral):
            return BooleanLiteral(self.value != other.value)
        else:
            return BooleanLiteral(True)
    def __repr__(self): 
        return str(self.value)

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def AsLiteral(self):
        return f"Variable({self.name})"
    
    def __repr__(self):
        return self.name


class FunctionDeclaration(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def AsLiteral(self):
        return f"FunctionDeclaration({self.name}, {self.parameters}, {self.body})"
    
    def __repr__(self):
        return f'function {self.name}'

class FunctionCall(Expression):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def AsLiteral(self):
        return f"FunctionCall({self.name}, {self.arguments})"
    
    def __repr__(self):
        return ''


class Assignment(Statement):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def AsLiteral(self):
        return f"Assignment({self.variable}, {self.value})"

    def __repr__(self):
        return ''

class AugmentedAssignment(Statement):
    """Examples: x += 2, x -= 2, x *= 2 , x /= 2, x ^= 2, etc"""
    def __init__(self, variable, op, value):
        self.variable = variable # E.g: x
        self.op = op # E.g: +=, -=, *=, /=, ^=, etc
        self.value = value # E.g: 5

    def AsLiteral(self):
        return f"AugmentedAssignment({self.variable}, {self.op}, {self.value})"

    def __repr__(self):
        return ''

class BinaryOperation(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def AsLiteral(self):
        return f"BinaryOperation({self.left}, {self.op}, {self.right})"

    def __repr__(self):
        return ''

class ComparisonOperation(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def AsLiteral(self):
        return f"ComparisonOperation({self.left}, {self.op}, {self.right})"
    
    def __repr__(self):
        return ''
    

class UnaryOperation(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def AsLiteral(self):
        return f"UnaryOperation({self.op}, {self.operand})"

    def __repr__(self):
        return f'UnaryOperation({self.op}, {self.operand})'
    

class VariableDeclaration(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def AsLiteral(self):
        return f"VariableDeclaration({self.name}, {self.value})"

    def __repr__(self):
        return ''
        

class IfStatement (Statement):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.if_body = body
        self.else_body = else_body

    def AsLiteral(self):
        return f"IfStatement({self.condition}, {self.if_body}, {self.else_body})"

    def __repr__(self):
        return ''
    
class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def AsLiteral(self):
        return f"WhileStatement({self.condition}, {self.body})"

    def __repr__(self):
        return ''
    
class ForStatement(Statement):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def AsLiteral(self):
        return f"ForStatement({self.init.AsLiteral()}, {self.condition.AsLiteral()}, {self.update.AsLiteral()})"

    def __repr__(self):
        return ''