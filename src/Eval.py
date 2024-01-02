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
            #print("VAR VALUE", type(scope[node.variable]))
            #print("BBBBB", type(self.evaluate(node.value, scope)))
            scope[node.variable] = self.perform_binary_operation(node.op, scope[node.variable], self.evaluate(node.value, scope), scope)

        elif isinstance(node, PTypes.BinaryOperation):
            if not isinstance(node.left, PTypes.Variable):
                left = self.evaluate(node.left, scope)
            else:
                left = node.left

            right = self.evaluate(node.right, scope)
            return self.perform_binary_operation(node.op, left, right, scope)

        elif isinstance(node, PTypes.UnaryOperation):
            return self.perform_unary_operation(node.op, self.evaluate(node.operand,scope))

        elif isinstance(node, PTypes.NumberLiteral):
            return node  # Return the NumberLiteral object itself

        elif isinstance(node, PTypes.StringLiteral):
            return node  # Return the StringLiteral object itself

        elif isinstance(node, PTypes.BooleanLiteral):
            return node

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
            if condition_value.value == True:
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
            #print("AEWAWEAWEAWE",self.evaluate(node.condition, scope))
            #print(node.AsLiteral())
            while self.evaluate(node.condition, scope).value == True:

                for statement in node.body:
                    
                    #print(statement.AsLiteral())
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


    def perform_comparison_operation(self, op, left: PTypes.DataType, right: PTypes.DataType):
        left = left if isinstance(left, PTypes.NumberLiteral) else left
        right = right if isinstance(right, PTypes.NumberLiteral) else right
        #print(left.AsLiteral(),right.AsLiteral(),op)
        if op == Token.TOKENTYPE.IS_EQUAL:
            #print(left.is_equal( right))
            return left.is_equal(right)
        elif op == Token.TOKENTYPE.NOT_EQUAL:
            return left.is_not_equal(right)
        elif op == Token.TOKENTYPE.LESS_THAN:
            return left.is_less_than(right)
        elif op == Token.TOKENTYPE.LESS_THAN_OR_EQUAL:
            return left.is_less_than_or_equal(right)
        elif op == Token.TOKENTYPE.GREATER_THAN:
            return left.is_greater_than(right)
        elif op == Token.TOKENTYPE.GREATER_THAN_OR_EQUAL:
            return left.is_greater_than_or_equal(right)
        else:
            raise Exception

    def perform_binary_operation(self, op, left: PTypes.NumberLiteral, right: PTypes.NumberLiteral, scope=None):
        left = self.evaluate(left, scope)
        right = self.evaluate(right, scope)
        if op == Token.TOKENTYPE.PLUS or op == Token.TOKENTYPE.PLUS_EQUAL:
            return left.add(right)
        elif op == Token.TOKENTYPE.MINUS or op == Token.TOKENTYPE.MINUS_EQUAL:
            return left.subtract(right)
        elif op == Token.TOKENTYPE.MUL or op == Token.TOKENTYPE.TIMES_EQUAL:
            return left.multiply(right)
        elif op == Token.TOKENTYPE.DIV or op == Token.TOKENTYPE.DIVIDE_EQUAL:
            return left.divide(right)
        elif op == Token.TOKENTYPE.MODULO or op == Token.TOKENTYPE.MODULO_EQUAL:
            return left.modulo(right)
        elif op == Token.TOKENTYPE.CARAT or op == Token.TOKENTYPE.CARAT_EQUAL:
            return left.power(right)
        else:
            raise Exception(f"Unsupported binary operation '{op}'")

    def perform_unary_operation(self, op, operand: PTypes.DataType):
        operand = operand.value if isinstance(operand, PTypes.NumberLiteral) else operand
        if op == Token.TOKENTYPE.MINUS:
            return operand.unary_minus()
        elif op == Token.TOKENTYPE.BANG:
            #print("BANG", operand.unary_not())
            return operand.unary_not()
        else:
            raise Exception(f"Unsupported unary operation '{op}'")

    std_functions = ["print","time","quit"]
    def handle_std_function_call(self, node, scope):
        if node.name == "print":
            a=[self.evaluate(i, scope) for i in node.arguments]
            print(*a)
        elif node.name == "time":
            import time
            return PTypes.NumberLiteral('float',time.time())
        elif node.name == "quit":
            exit()
        else:
            raise Exception(f"Unknown standard function '{node.name}'")
    def handle_method_call(self, node: PTypes.MethodCall, scope):
        variable = node.variable
        method = node.method
        arguments = node.arguments
        n_args = [self.evaluate(arg, scope) for arg in arguments]
        #print(variable, method, arguments, scope)
        var_value = self.evaluate(variable, scope)
        variable_methods = var_value.methods if hasattr(var_value, "methods") else {}
        if method in variable_methods:
            return variable_methods[method](n_args)
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
    program = """var x = 12
    var y = 15 == 15
    print(!!y)
    """
    tokens = Lexer.tokenize(program)
    #print(tokens)
    ast = Parser.parse_program(tokens)
    for i in ast:
        print(i.AsLiteral())
    ev.execute(ast)
