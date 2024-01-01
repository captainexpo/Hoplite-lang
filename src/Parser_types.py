class Statement:
    def __repr__(self):
        return "Statement()"
    
    def AsLiteral(self):
        return None

class Expression:
    def __repr__(self):
        return "Expression()"
    def AsLiteral(self):
        return None
    

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
    
    def AsLiteral(self):
        return self.value

class MethodCall(Expression):
    def __init__(self, variable, method_name, arguments):
        self.variable = variable
        self.method = method_name
        self.arguments = arguments

    def __repr__(self):
        arguments_str = ", ".join([str(arg) for arg in self.arguments])
        return f"MethodCall({self.variable}, {self.method}, [{arguments_str}])"

class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral({self.value})"
    
    def AsLiteral(self):
        return self.value

class ArrayLiteral(Expression):
    def __init__(self, elements):
        self.elements = elements
        print("AWEAWEAWEAWE",self.elements)
        self.methods = {
            "append": lambda item: self.elements.append(item),
            "pop": lambda: self.elements.pop(),
            "at": lambda index: self.elements[index],
        }
        
    def __repr__(self):
        return f"ArrayLiteral({self.elements})"
    
    def AsLiteral(self):
        output = "["
        for i in self.elements:
            print(i)
            output += f"{i.AsLiteral()}, "
        output = output[:-2]
        output += "]"
        return output

class BooleanLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"BooleanLiteral({self.value})"
    
    def AsLiteral(self):
        return self.value == "true"

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"
    
    def AsLiteral(self):
        return self.name


class FunctionDeclaration(Statement):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"FunctionDeclaration({self.name}, {self.parameters}, {self.body})"
    
    def AsLiteral(self):
        return f'function {self.name}'

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

class AugmentedAssignment(Statement):
    """Examples: x += 2, x -= 2, x *= 2 , x /= 2, x ^= 2, etc"""
    def __init__(self, variable, op, value):
        self.variable = variable # E.g: x
        self.op = op # E.g: +=, -=, *=, /=, ^=, etc
        self.value = value # E.g: 5

    def __repr__(self):
        return f"AugmentedAssignment({self.variable} {self.op}  {self.value})"

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
    
    def AsLiteral(self):
        return self.value

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

class ForStatement(Statement):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f"ForStatement({self.init}, {self.condition}, {self.update}, {self.body})"