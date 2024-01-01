import Parser_types as PTypes
import Tokens as Token
import Lexer as Lexer
import Parser as Parser
class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Evaluator:
    def __init__(self):
        self.global_symbol_table = {}

    def evaluate(self, node, local_scope=None):
        scope = local_scope if local_scope is not None else self.global_symbol_table

        if isinstance(node, PTypes.FunctionDeclaration):
            self.global_symbol_table[node.name] = node

        elif isinstance(node, PTypes.VariableDeclaration):
            scope[node.name] = self.evaluate(node.value, scope)

        elif isinstance(node, PTypes.Assignment):
            scope[node.variable] = self.evaluate(node.value, scope)

        elif isinstance(node, PTypes.AugmentedAssignment):
            scope[node.variable] = self.perform_binary_operation(node.op, scope[node.variable], self.evaluate(node.value, scope))

        elif isinstance(node, PTypes.BinaryOperation):
            if not isinstance(node.left, PTypes.Variable):
                left = self.evaluate(node.left, scope)
            else:
                left = node.left

            right = self.evaluate(node.right, scope)
            return self.perform_binary_operation(node.op, left, right)

        elif isinstance(node, PTypes.UnaryOperation):
            operand = self.evaluate(node.operand, scope)
            return self.perform_unary_operation(node.op, operand)

        elif isinstance(node, PTypes.NumberLiteral):
            return node  # Return the NumberLiteral object itself

        elif isinstance(node, PTypes.StringLiteral):
            return node  # Return the StringLiteral object itself

        elif isinstance(node, PTypes.BooleanLiteral):
            return node.value == 'true'

        elif isinstance(node, PTypes.Variable):
            var_value = scope.get(node.name)
            if var_value is None:
                raise Exception(f"Undefined variable '{node.name}'")
            return var_value

        elif isinstance(node, PTypes.ArrayLiteral):
            return PTypes.ArrayLiteral([self.evaluate(element, scope) for element in node.elements])

        elif isinstance(node, PTypes.FunctionCall):
            return self.handle_function_call(node, scope)

        elif isinstance(node, PTypes.IfStatement):
            condition_value = self.evaluate(node.condition, scope)
            if condition_value:
                for statement in node.if_body:
                    result = self.evaluate(statement, scope)
                    if isinstance(result, ReturnValue):
                        return result.value
            elif node.else_body:
                for statement in node.else_body:
                    result = self.evaluate(statement, scope)
                    if isinstance(result, ReturnValue):
                        return result.value

        elif isinstance(node, PTypes.ReturnStatement):
            return ReturnValue(self.evaluate(node.value, scope))

        elif isinstance(node, PTypes.WhileStatement):
            while self.evaluate(node.condition, scope):
                for statement in node.body:
                    result = self.evaluate(statement, scope)
                    if isinstance(result, ReturnValue):
                        return result.value

        elif isinstance(node, PTypes.ForStatement):
            self.evaluate(node.init, scope)
            while self.evaluate(node.condition, scope):
                for statement in node.body:
                    result = self.evaluate(statement, scope)
                    if isinstance(result, ReturnValue):
                        return result.value
                self.evaluate(node.update, scope)

        elif isinstance(node, PTypes.MethodCall):
            return self.handle_method_call(node, scope)

        elif isinstance(node, PTypes.ComparisonOperation):
            left = self.evaluate(node.left, scope)
            right = self.evaluate(node.right, scope)
            return self.perform_comparison_operation(node.op, left, right)

        else:
            raise Exception(f"Unknown node type '{node}'")


    def perform_comparison_operation(self, op, left, right):
        left = left.value if isinstance(left, PTypes.NumberLiteral) else left
        right = right.value if isinstance(right, PTypes.NumberLiteral) else right
        if op == Token.TOKENTYPE.EQUALS:
            return PTypes.BooleanLiteral(left == right)
        elif op == Token.TOKENTYPE.NOT_EQUAL:
            return PTypes.BooleanLiteral(left != right)
        elif op == Token.TOKENTYPE.LESS_THAN:
            return PTypes.BooleanLiteral(left < right)
        elif op == Token.TOKENTYPE.LESS_THAN_OR_EQUAL:
            return PTypes.BooleanLiteral(left <= right)
        elif op == Token.TOKENTYPE.GREATER_THAN:
            return PTypes.BooleanLiteral(left > right)
        elif op == Token.TOKENTYPE.GREATER_THAN_OR_EQUAL:
            return PTypes.BooleanLiteral(left >= right)
        else:
            raise Exception(f"Unsupported comparison operation '{op}'")

    def perform_binary_operation(self, op, left: PTypes.NumberLiteral, right: PTypes.NumberLiteral):
        left = left.value if isinstance(left, PTypes.NumberLiteral) else self.evaluate(left)
        print(left.type, right.type)
        print(left.value, right.value)
        right = right.value
        print(type(left), type(right))
        print(left, right)
        if op == Token.TOKENTYPE.PLUS or op == Token.TOKENTYPE.PLUS_EQUAL:
            return left.Add(right)
        elif op == Token.TOKENTYPE.MINUS or op == Token.TOKENTYPE.MINUS_EQUAL:
            return left.Subtract(right)
        elif op == Token.TOKENTYPE.MUL or op == Token.TOKENTYPE.TIMES_EQUAL:
            return left.Multiply(right)
        elif op == Token.TOKENTYPE.DIV or op == Token.TOKENTYPE.DIVIDE_EQUAL:
            return left.Divide(right)
        elif op == Token.TOKENTYPE.MODULO or op == Token.TOKENTYPE.MODULO_EQUAL:
            return left.Modulo(right)
        elif op == Token.TOKENTYPE.CARAT or op == Token.TOKENTYPE.CARAT_EQUAL:
            return left.Power(right)
        else:
            raise Exception(f"Unsupported binary operation '{op}'")

    def perform_unary_operation(self, op, operand):
        operand = operand.value if isinstance(operand, PTypes.NumberLiteral) else operand
        if op == Token.TOKENTYPE.MINUS:
            return PTypes.NumberLiteral('',-operand)
        elif op == Token.TOKENTYPE.BANG:
            return PTypes.BooleanLiteral(not operand)
        else:
            raise Exception(f"Unsupported unary operation '{op}'")

    std_functions = ["print","time"]
    def handle_std_function_call(self, node, scope):
        if node.name == "print":
            print(self.evaluate(node.arguments[0], scope))
        elif node.name == "time":
            import time
            return PTypes.NumberLiteral('float',time.time())
        else:
            raise Exception(f"Unknown standard function '{node.name}'")
    def handle_method_call(self, node: PTypes.MethodCall, scope):
        variable = node.variable
        method = node.method
        arguments = node.arguments
        var_value = self.evaluate(variable, scope)
        variable_methods = var_value.methods if hasattr(var_value, "methods") else {}
        if method in variable_methods:
            return variable_methods[method](arguments)
        else:
            raise Exception(f"Variable '{variable.name}' does not have method '{method}'")


    def handle_function_call(self, node, scope):
        if node.name in self.std_functions:
            return self.handle_std_function_call(node, scope)

        func = self.global_symbol_table.get(node.name)
        if not func:
            raise Exception(f"Function '{node.name}' not defined")

        if len(node.arguments) != len(func.parameters):
            raise Exception(f"Expected {len(func.parameters)} arguments, got {len(node.arguments)}")

        local_scope = {param: self.evaluate(arg, scope) for param, arg in zip(func.parameters, node.arguments)}
        try:
            for statement in func.body:
                result = self.evaluate(statement, local_scope)
                if isinstance(statement, PTypes.ReturnStatement):
                    return result
        except ReturnValue as returnValue:
            return returnValue.value

    def execute(self, ast):
        results = []
        for node in ast:
            result = self.evaluate(node)
            if result is not None:
                results.append(result)
        return results

# Example usage
if __name__ == "__main__":
    ev = Evaluator()
    program = """
    var x = [2]
    x.append(3)
    print(x)
    print("POPPING")
    print(x.pop())
    for (var i = 0; i < 10; i = i + 1) {
        print(i)
    }
    x.append([4,5,6])
    print(x)
    """
    tokens = Lexer.tokenize(program)
    print(tokens)
    ast = Parser.parse_program(tokens)
    for i in ast:
        print(i.AsLiteral())
    ev.execute(ast)
