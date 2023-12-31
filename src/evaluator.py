import token_class as Token
class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value
        
class Evaluator:
    def __init__(self):
        self.global_symbol_table = {}
        self.call_stack = []  # Call stack for function calls
    def evaluate(self, node, local_scope=None):
        scope = local_scope if local_scope is not None else self.global_symbol_table

        if node['type'] == 'variable_declaration':
            scope[node['name']] = self.evaluate(node['value'], local_scope)
        elif node['type'] == 'assignment':
            updated_scope = local_scope if local_scope and node['name'] in local_scope else self.global_symbol_table
            updated_scope[node['name']] = self.evaluate(node['value'], local_scope)
        elif node['type'] == 'binary_operation':
            left = self.evaluate(node['left'], local_scope)
            right = self.evaluate(node['right'], local_scope)
            if node['op'] == Token.TOKENTYPE.PLUS:
                return left + right
            elif node['op'] == Token.TOKENTYPE.MINUS:
                return left - right
            elif node['op'] == Token.TOKENTYPE.MUL:
                return left * right
            elif node['op'] == Token.TOKENTYPE.DIV:
                return left / right
            elif node['op'] == Token.TOKENTYPE.MODULO:
                return left % right
            elif node['op'] == Token.TOKENTYPE.CARAT:
                return left ** right
            
        elif node['type'] == 'integer':
            return int(node['value'])
        elif node['type'] == 'float':
            return float(node['value'])
        elif node['type'] == 'string':
            return str(node['value'])
        elif node['type'] == 'variable':
            if node['name'] in scope:
                return scope[node['name']]
            else:
                raise Exception(f"Undefined variable '{node['name']}'")
        elif node['type'] == 'function_declaration':
            self.global_symbol_table[node['name']] = {
                "parameters": node['parameters'],
                "body": node['body']
            }
        elif node['type'] == 'if_statement':
            condition_value = self.evaluate(node['condition'], local_scope)
            if condition_value:
                for statement in node['if_body']:
                    result = self.evaluate(statement, local_scope)
                    if statement['type'] == 'return':
                        return result  # Propagate return value up
            else:
                if node['else_body'] is not None:
                    for statement in node['else_body']:
                        result = self.evaluate(statement, local_scope)
                        if statement['type'] == 'return':
                            return result  # Propagate return value up
        # Add support for comparison operators (==, >=, <=, >, <, etc.)
        elif node['type'] == 'comparison_operation':
            left = self.evaluate(node['left'], local_scope)
            right = self.evaluate(node['right'], local_scope)
            #print(left,right, end=" | ")
            if node['op'] == Token.TOKENTYPE.LESS_THAN:
                result = left < right
            elif node['op'] == Token.TOKENTYPE.GREATER_THAN:
                result = left > right
            elif node['op'] == Token.TOKENTYPE.LESS_THAN_OR_EQUAL:
                result = left <= right
            elif node['op'] == Token.TOKENTYPE.GREATER_THAN_OR_EQUAL:
                result = left >= right
            elif node['op'] == Token.TOKENTYPE.IS_EQUAL:
                #print(left, right, end=": ")
                result = left == right
            #print("RESULT: ", result)
            return result
        elif node['type'] == 'while_statement':
            while self.evaluate(node['condition'], local_scope) == True:
                for statement in node['body']:
                    self.evaluate(statement, local_scope)
        elif node['type'] in ['true', 'false']:
            return True if node['type'] == 'true' else False
        elif node['type'] == 'function_call':
            func = self.global_symbol_table.get(node['name'])
            if node['name'] == 'print':
                print(self.evaluate(node['arguments'][0], local_scope))
                return
            elif node['name'] == 'time':
                import time
                return time.time()
            elif node['name'] == 'input':
                return input()
            elif node['name'] == 'quit':
                exit()
            if not func:
                raise Exception(f"Function '{node['name']}' not defined")

            # Prepare the local scope for the function call
            local_scope = dict(zip(func['parameters'], [self.evaluate(arg, local_scope) for arg in node['arguments']]))
            self.call_stack.append(local_scope)

            try:
                for statement in func['body']:
                    self.evaluate(statement, local_scope)
            except ReturnValue as returnValue:
                self.call_stack.pop()
                return returnValue.value  # Return the value from ReturnValue

            self.call_stack.pop()
            if len(node['arguments']) != len(func['parameters']):
                raise Exception(f"Expected {len(func['parameters'])} arguments, got {len(node['arguments'])}")

            local_scope = dict(zip(func['parameters'], [self.evaluate(arg, local_scope) for arg in node['arguments']]))
            self.call_stack.append(local_scope)

            for statement in func['body']:
                result = self.evaluate(statement, local_scope)
                if statement['type'] == 'return':
                    self.call_stack.pop()
                    return result  # Propagate the return value up

            self.call_stack.pop()
        elif node['type'] == 'return':
            #print("RETURNING: ", self.evaluate(node['value'], local_scope))
            raise ReturnValue(self.evaluate(node['value'], local_scope))
        else:
            raise Exception(f"Unknown node type \'{node['type']}\'" )

    def execute(self, ast):
        for node in ast:
            try:
                self.evaluate(node)
            except Exception as e:
                with open("debug.log", "w") as f:
                    # write detailed error message to debug.log
                    f.write(str(e))
                print("ERROR:", str(e))
                quit(-1)

        return self.global_symbol_table
    

if __name__ == "__main__":
    ev = Evaluator()
    program = """
    mkfunc factorial(x){

        if (x == 1) {
            return 1
        }
        return x * factorial(x - 1)
    }
    print(factorial(5))
    """
    import lexer_class
    import parser_class
    tokens = lexer_class.tokenize(program)
    ast = parser_class.parse_program(tokens)
    ev.execute(ast)
