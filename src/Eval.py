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
            
            right = self.evaluate(node.value, scope)
            if node.op == Token.TOKENTYPE.PLUS_EQUAL:
                scope[node.variable] += right
            elif node.op == Token.TOKENTYPE.MINUS_EQUAL:
                scope[node.variable] -= right
            elif node.op == Token.TOKENTYPE.TIMES_EQUAL:
                scope[node.variable] *= right
            elif node.op == Token.TOKENTYPE.DIVIDE_EQUAL:
                scope[node.variable] /= right
            elif node.op == Token.TOKENTYPE.MODULO_EQUAL:
                scope[node.variable] %= right
            elif node.op == Token.TOKENTYPE.CARAT_EQUAL:
                scope[node.variable] **= right
        elif isinstance(node, PTypes.BinaryOperation):
            left = self.evaluate(node.left, scope)
            right = self.evaluate(node.right, scope)
            return self.perform_binary_operation(node.op, left, right)

        elif isinstance(node, PTypes.UnaryOperation):
            operand = self.evaluate(node.operand, scope)
            return self.perform_unary_operation(node.op, operand)

        elif isinstance(node, PTypes.NumberLiteral):
            return int(node.value) if node.type == 'int' else float(node.value)

        elif isinstance(node, PTypes.StringLiteral):
            return node.value

        elif isinstance(node, PTypes.BooleanLiteral):
            return node.value == 'true'

        elif isinstance(node, PTypes.Variable):
            if node.name in scope:
                return scope[node.name]
            else:
                raise Exception(f"Undefined variable '{node.name}'")
        elif isinstance(node, PTypes.ArrayLiteral):
            return [self.evaluate(element, scope) for element in node.elements]
        elif isinstance(node, PTypes.FunctionCall):
            return self.handle_function_call(node, scope)
        elif isinstance(node, PTypes.IfStatement):
            condition_value = self.evaluate(node.condition, local_scope)
            if condition_value:
                for statement in node.if_body:
                    result = self.evaluate(statement, local_scope)
                    if isinstance(statement, PTypes.ReturnStatement):
                        return result
            elif node.else_body is not None:
                for statement in node.else_body:
                    result = self.evaluate(statement, local_scope)
                    if isinstance(statement, PTypes.ReturnStatement):
                        return result
        elif isinstance(node, PTypes.ReturnStatement):
            raise ReturnValue(self.evaluate(node.value, scope))
        elif isinstance(node, PTypes.WhileStatement):
            while self.evaluate(node.condition, local_scope):
                for statement in node.body:
                    result = self.evaluate(statement, local_scope)
                    if isinstance(statement, PTypes.ReturnStatement):
                        return result
        elif isinstance(node, PTypes.ForStatement):
            self.evaluate(node.init, local_scope)
            while self.evaluate(node.condition, local_scope):
                for statement in node.body:
                    result = self.evaluate(statement, local_scope)
                    if isinstance(statement, PTypes.ReturnStatement):
                        return result
                self.evaluate(node.update, local_scope)
        elif isinstance(node, PTypes.MethodCall):
            return self.handle_method_call(node, scope)
        elif isinstance(node, PTypes.ComparisonOperation):
            left = self.evaluate(node.left, scope)
            right = self.evaluate(node.right, scope)
            if node.op == Token.TOKENTYPE.IS_EQUAL:
                return left == right
            elif node.op == Token.TOKENTYPE.NOT_EQUAL:
                return left != right
            elif node.op == Token.TOKENTYPE.GREATER_THAN:
                return left > right
            elif node.op == Token.TOKENTYPE.GREATER_THAN_OR_EQUAL:
                return left >= right
            elif node.op == Token.TOKENTYPE.LESS_THAN:
                return left < right
            elif node.op == Token.TOKENTYPE.LESS_THAN_OR_EQUAL:
                return left <= right
        else:
            raise Exception(f"Unknown node type '{node}'")

    def perform_binary_operation(self, op, left, right):
        if op == Token.TOKENTYPE.PLUS:
            return left + right
        elif op == Token.TOKENTYPE.MINUS:
            return left - right
        elif op == Token.TOKENTYPE.MUL:
            return left * right
        elif op == Token.TOKENTYPE.DIV:
            return left / right
        elif op == Token.TOKENTYPE.MODULO:
            return left % right
        elif op == Token.TOKENTYPE.CARAT:
            return left ** right
        else:
            raise Exception(f"Unsupported binary operation '{op}'")

    def perform_unary_operation(self, op, operand):
        if op == Token.TOKENTYPE.MINUS:
            return -operand
        elif op == Token.TOKENTYPE.BANG:
            return not operand
        else:
            raise Exception(f"Unsupported unary operation '{op}'")

    std_functions = ["print","time"]
    def handle_std_function_call(self, node, scope):
        if node.name == "print":
            print(self.evaluate(node.arguments[0], scope))
        elif node.name == "time":
            import time
            return time.time()
        else:
            raise Exception(f"Unknown standard function '{node.name}'")
    def handle_method_call(self, node: PTypes.MethodCall, scope):
        variable = node.variable
        method = node.method
        arguments = node.arguments
        var_value = self.evaluate(variable, scope)
        print(var_value,variable)
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
    """
    tokens = Lexer.tokenize(program)
    print(tokens)
    ast = Parser.parse_program(tokens)
    print(ast)
    results = ev.execute(ast)
    for result in results:
        print(result)
