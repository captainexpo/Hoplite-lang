import token_class as Token

class Parser:
    def __init__(self, tokens=None):
        self.tokens = tokens
        self.pos = 0

    def error(self, message="Invalid syntax"):
        raise Exception(message)

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        if self.current_token() and self.current_token().type == token_type:
            self.pos += 1
        else:
            self.error(f"Expected token: {token_type}, found: {self.current_token()}")
    def get_statement(self):
        if self.current_token().type == Token.TOKENTYPE.COMMENT:
            self.eat(Token.TOKENTYPE.COMMENT)
        elif self.current_token().type == Token.TOKENTYPE.WHILE:
            return self.parse_while_statement()
        elif self.current_token().type == Token.TOKENTYPE.FUNCTION_DECLARATION:
            return self.parse_function_declaration()
        elif self.current_token().type == Token.TOKENTYPE.VAR:
            return self.parse_variable_declaration()
        elif self.current_token().type == Token.TOKENTYPE.NAME:
            lookahead_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if lookahead_token and lookahead_token.type == Token.TOKENTYPE.LPAREN:
                return self.parse_function_call()
            else:
                return self.parse_assignment()
        elif self.current_token().type == Token.TOKENTYPE.IF:
            return self.parse_if_statement()
        elif self.current_token().type == Token.TOKENTYPE.ELSE:
            return self.parse_else_statement()
        else:
            self.error("Unexpected token " + self.current_token().type)
    def parse(self):
        statements = []
        while self.current_token() is not None:
            statements.append(self.get_statement())
        return statements


    def parse_function_declaration(self):
        self.eat(Token.TOKENTYPE.FUNCTION_DECLARATION)
        func_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.LPAREN)
        parameters = self.parse_parameters()
        self.eat(Token.TOKENTYPE.RPAREN)
        self.eat(Token.TOKENTYPE.LBRACE)
        body = self.parse_block()
        self.eat(Token.TOKENTYPE.RBRACE)
        return {"type": "function_declaration", "name": func_name, "parameters": parameters, "body": body}

    def parse_function_call(self):
        func_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.LPAREN)
        arguments = self.parse_arguments()
        self.eat(Token.TOKENTYPE.RPAREN)
        return {"type": "function_call", "name": func_name, "arguments": arguments}

    def parse_arguments(self):
        arguments = []
        while self.current_token().type != Token.TOKENTYPE.RPAREN:
            arguments.append(self.parse_expression())
            if self.current_token().type == Token.TOKENTYPE.COMMA:
                self.eat(Token.TOKENTYPE.COMMA)
        return arguments
    
    def parse_list(self):
        values = []
        while self.current_token().type != Token.TOKENTYPE.RBRACK:
            values.append(self.parse_expression())
            if self.current_token().type == Token.TOKENTYPE.COMMA:
                self.eat(Token.TOKENTYPE.COMMA)
    def parse_parameters(self):
        parameters = []
        while self.current_token().type != Token.TOKENTYPE.RPAREN:
            parameters.append(self.current_token().value)
            self.eat(Token.TOKENTYPE.NAME)
            if self.current_token().type == Token.TOKENTYPE.COMMA:
                self.eat(Token.TOKENTYPE.COMMA)
        return parameters

    def parse_block(self):
        statements = []
        while self.current_token().type != Token.TOKENTYPE.RBRACE:
            if self.current_token().type == Token.TOKENTYPE.COMMENT:
                self.eat(Token.TOKENTYPE.COMMENT)
            elif self.current_token().type == Token.TOKENTYPE.WHILE:
                statements.append(self.parse_while_statement())
            elif self.current_token().type == Token.TOKENTYPE.IF:
                statements.append(self.parse_if_statement())
            
            elif self.current_token().type == Token.TOKENTYPE.RETURN:
                statements.append(self.parse_return_statement())
            elif self.current_token().type == Token.TOKENTYPE.VAR:
                statements.append(self.parse_variable_declaration())
            elif self.current_token().type == Token.TOKENTYPE.NAME:
                lookahead_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
                if lookahead_token and lookahead_token.type == Token.TOKENTYPE.LPAREN:
                    statements.append(self.parse_function_call())
                else:
                    statements.append(self.parse_assignment())
            else:
                self.error("Unexpected token in block " + self.current_token().type)
        return statements
    def parse_return_statement(self):
        self.eat(Token.TOKENTYPE.RETURN)
        expr = self.parse_expression()
        return {"type": "return", "value": expr}

    def parse_variable_declaration(self):
        self.eat(Token.TOKENTYPE.VAR)
        var_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.EQUALS)
        expr = self.parse_expression()
        return {"type": "variable_declaration", "name": var_name, "value": expr}

    def parse_assignment(self):
        var_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.EQUALS)
        expr = self.parse_expression()
        return {"type": "assignment", "name": var_name, "value": expr}

    def parse_expression(self):
        node = self.parse_term()

        while self.current_token() is not None and self.current_token().type in (
            Token.TOKENTYPE.IS_EQUAL, Token.TOKENTYPE.GREATER_THAN_OR_EQUAL,
            Token.TOKENTYPE.LESS_THAN_OR_EQUAL, Token.TOKENTYPE.GREATER_THAN,
            Token.TOKENTYPE.LESS_THAN
        ):
            token_type = self.current_token().type
            self.eat(token_type)
            node = {"type": "comparison_operation", "left": node, "op": token_type, "right": self.parse_term()}

        return node

    def parse_term(self):
        node = self.parse_factor()

        while self.current_token() is not None and self.current_token().type in (Token.TOKENTYPE.PLUS, Token.TOKENTYPE.MINUS, Token.TOKENTYPE.MODULO, Token.TOKENTYPE.CARAT):
            token_type = self.current_token().type
            self.eat(token_type)
            node = {"type": "binary_operation", "left": node, "op": token_type, "right": self.parse_factor()}

        return node

    def parse_factor(self):
        node = self.parse_atom()

        while self.current_token() is not None and self.current_token().type in (Token.TOKENTYPE.MUL, Token.TOKENTYPE.DIV):
            token_type = self.current_token().type
            self.eat(token_type)
            node = {"type": "binary_operation", "left": node, "op": token_type, "right": self.parse_atom()}

        return node

    def parse_atom(self):
        token = self.current_token()
        if token.type == Token.TOKENTYPE.INTEGER:
            self.eat(Token.TOKENTYPE.INTEGER)
            return {"type": "integer", "value": token.value}
        if token.type == Token.TOKENTYPE.STRING:
            self.eat(Token.TOKENTYPE.STRING)
            token.value = token.value[1:-1]
            return {"type": "string", "value": token.value}
        elif token.type == Token.TOKENTYPE.FLOAT:
            self.eat(Token.TOKENTYPE.FLOAT)
            return {"type": "float", "value": token.value}
        elif token.type == Token.TOKENTYPE.TRUE:
            self.eat(Token.TOKENTYPE.TRUE)
            return {"type": "true"}
        elif token.type == Token.TOKENTYPE.FALSE:
            self.eat(Token.TOKENTYPE.FALSE)
            return {"type": "false"}
        elif token.type == Token.TOKENTYPE.NAME:
            # Check if it's a function call
            lookahead_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if lookahead_token and lookahead_token.type == Token.TOKENTYPE.LPAREN:
                return self.parse_function_call()
            else:
                self.eat(Token.TOKENTYPE.NAME)
                return {"type": "variable", "name": token.value}
        elif token.type == Token.TOKENTYPE.LPAREN:
            self.eat(Token.TOKENTYPE.LPAREN)
            node = self.parse_expression()
            self.eat(Token.TOKENTYPE.RPAREN)
            return node
        else:
            self.error(f"Unknown atom {token}")
    def parse_if_statement(self):
        self.eat(Token.TOKENTYPE.IF)
        self.eat(Token.TOKENTYPE.LPAREN)
        condition = self.parse_expression()
        self.eat(Token.TOKENTYPE.RPAREN)
        self.eat(Token.TOKENTYPE.LBRACE)
        if_body = self.parse_block()
        self.eat(Token.TOKENTYPE.RBRACE)
        else_body = None
        if self.current_token() and self.current_token().type == Token.TOKENTYPE.ELSE:
            else_body = self.parse_else_statement()
        return {"type": "if_statement", "condition": condition, "if_body": if_body, "else_body": else_body}
    def parse_else_statement(self):
        self.eat(Token.TOKENTYPE.ELSE)
        self.eat(Token.TOKENTYPE.LBRACE)
        else_body = self.parse_block()
        self.eat(Token.TOKENTYPE.RBRACE)
        return else_body
    def parse_while_statement(self):
        self.eat(Token.TOKENTYPE.WHILE)
        self.eat(Token.TOKENTYPE.LPAREN)
        condition = self.parse_expression()
        self.eat(Token.TOKENTYPE.RPAREN)
        self.eat(Token.TOKENTYPE.LBRACE)
        body = self.parse_block()
        self.eat(Token.TOKENTYPE.RBRACE)
        return {"type": "while_statement", "condition": condition, "body": body}

def parse_program(tokens):
    parser = Parser(tokens)
    return parser.parse()

if __name__ == "__main__":
    import lexer_class, json
    program =  """
    mkfunc factorial(x){
        if (x == 1){
            return 1
        }
        return x * factorial(x - 1)
    }
    print(factorial(5))"""
    print(program)
    tokens = lexer_class.tokenize(program)
    print(json.dumps(parse_program(tokens),indent=4))
