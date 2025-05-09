import Tokens as Token
from Parser_types import *
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
        elif self.current_token().type == Token.TOKENTYPE.FOR:
            return self.parse_for_loop()
        
        elif self.current_token().type == Token.TOKENTYPE.FUNCTION_DECLARATION:
            return self.parse_function_declaration()
        elif self.current_token().type == Token.TOKENTYPE.VAR:
            return self.parse_variable_declaration()
        elif self.current_token().type in Token.AUGMENTED_ASSIGNMENT_OPERATORS:
            return self.parse_augmented_assignment()
        elif self.current_token().type == Token.TOKENTYPE.NAME:
            lookahead_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if lookahead_token and lookahead_token.type in Token.AUGMENTED_ASSIGNMENT_OPERATORS:
                return self.parse_augmented_assignment()
            elif lookahead_token and lookahead_token.type == Token.TOKENTYPE.LPAREN:
                return self.parse_function_call()
            elif lookahead_token and lookahead_token.type == Token.TOKENTYPE.DOT:
                return self.parse_method_call(Variable(self.current_token().value))
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
        while self.current_token() is not None and self.current_token().type != Token.TOKENTYPE.EOF:
            statements.append(self.get_statement())
        return statements

    def parse_for_loop(self):
        self.eat(Token.TOKENTYPE.FOR)
        self.eat(Token.TOKENTYPE.LPAREN)

        # Initial expression - can be a variable declaration or any expression
        init = None
        if self.current_token().type == Token.TOKENTYPE.VAR:
            init = self.parse_variable_declaration()
        else:
            init = self.parse_expression()
            if isinstance(init, Expression):
                init = init.expr  # unwrap expression from statement if needed
        self.eat(Token.TOKENTYPE.SEMICOLON)

        # Condition - any expression
        condition = self.parse_expression()
        self.eat(Token.TOKENTYPE.SEMICOLON)

        # Update - can be an assignment or any expression
        update = None
        if self.current_token().type == Token.TOKENTYPE.NAME:
            if self.tokens[self.pos + 1].type in Token.AUGMENTED_ASSIGNMENT_OPERATORS:
                update = self.parse_augmented_assignment()
            else:
                update = self.parse_assignment()
        else:
            update = self.parse_expression()

        self.eat(Token.TOKENTYPE.RPAREN)
        self.eat(Token.TOKENTYPE.LBRACE)
        body = self.parse_block()
        self.eat(Token.TOKENTYPE.RBRACE)

        return ForStatement(init, condition, update, body)

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
        return FunctionDeclaration(func_name, parameters, body)

    def parse_function_call(self):
        func_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.LPAREN)
        arguments = self.parse_arguments()
        self.eat(Token.TOKENTYPE.RPAREN)
        return FunctionCall(func_name, arguments)

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
                elif lookahead_token and lookahead_token.type in Token.AUGMENTED_ASSIGNMENT_OPERATORS:
                    statements.append(self.parse_augmented_assignment())
                else:
                    statements.append(self.parse_assignment())
            else:
                self.error("Unexpected token in block " + self.current_token().type)
        return statements
    def parse_return_statement(self):
        self.eat(Token.TOKENTYPE.RETURN)
        expr = self.parse_expression()
        return ReturnStatement(expr)

    def parse_variable_declaration(self):
        self.eat(Token.TOKENTYPE.VAR)
        var_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.EQUALS)
        expr = self.parse_expression()
        return VariableDeclaration(var_name, expr)

    def parse_augmented_assignment(self):
        # get asssignment as variable_name, operator, right hand side
        var_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        operator = self.current_token().type
        self.eat(operator)
        expr = self.parse_expression()
        print(var_name,operator,expr)
        return AugmentedAssignment(var_name, operator, expr)
    def parse_assignment(self):
        var_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.EQUALS)
        expr = self.parse_expression()
        return Assignment(var_name, expr)

    def parse_expression(self):
        node = self.parse_term()
    
        while self.current_token() is not None and self.current_token().type in Token.COMPARISON_OPERATORS:
            token_type = self.current_token().type
            self.eat(token_type)
            node = ComparisonOperation(node, token_type, self.parse_term())

        return node

    def parse_term(self):
        node = self.parse_factor()

        while self.current_token() is not None and self.current_token().type in (Token.TOKENTYPE.PLUS, Token.TOKENTYPE.MINUS, Token.TOKENTYPE.MODULO, Token.TOKENTYPE.CARAT):
            token_type = self.current_token().type
            self.eat(token_type)
            node = BinaryOperation(node, token_type, self.parse_factor())

        return node

    def parse_factor(self):
        node = self.parse_atom()

        while self.current_token() is not None and self.current_token().type in (Token.TOKENTYPE.MUL, Token.TOKENTYPE.DIV):
            token_type = self.current_token().type
            self.eat(token_type)
            node = BinaryOperation(node, token_type, self.parse_atom())

        return node

    def parse_array_literal(self):
        self.eat(Token.TOKENTYPE.LBRACK)
        elements = []
        if self.current_token().type != Token.TOKENTYPE.RBRACK:
            elements.append(self.parse_expression())
            while self.current_token().type == Token.TOKENTYPE.COMMA:
                self.eat(Token.TOKENTYPE.COMMA)
                elements.append(self.parse_expression())
        self.eat(Token.TOKENTYPE.RBRACK)
        return ArrayLiteral(elements)
    def parse_method_call(self, variable):
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.DOT)
        method_name = self.current_token().value
        self.eat(Token.TOKENTYPE.NAME)
        self.eat(Token.TOKENTYPE.LPAREN)
        arguments = self.parse_arguments()
        self.eat(Token.TOKENTYPE.RPAREN)
        return MethodCall(variable, method_name, arguments)
    def parse_atom(self):
        token = self.current_token()
        if token.type == Token.TOKENTYPE.BANG:
            self.eat(Token.TOKENTYPE.BANG)
            operand = self.parse_atom()
            return UnaryOperation(Token.TOKENTYPE.BANG,operand)
        elif token.type == Token.TOKENTYPE.MINUS:
            self.eat(Token.TOKENTYPE.MINUS)
            operand = self.parse_atom()
            #print(UnaryOperation(operand, Token.TOKENTYPE.MINUS))
            return UnaryOperation(Token.TOKENTYPE.MINUS, operand)
        elif token.type == Token.TOKENTYPE.INTEGER:
            self.eat(Token.TOKENTYPE.INTEGER)
            return NumberLiteral("int", token.value)
        elif token.type == Token.TOKENTYPE.STRING:
            self.eat(Token.TOKENTYPE.STRING)
            token.value = token.value[1:-1]
            return StringLiteral(token.value)
        elif token.type == Token.TOKENTYPE.FLOAT:
            self.eat(Token.TOKENTYPE.FLOAT)
            return NumberLiteral("float", token.value)
        elif token.type == Token.TOKENTYPE.TRUE:
            self.eat(Token.TOKENTYPE.TRUE)
            return BooleanLiteral("true")
        elif token.type == Token.TOKENTYPE.FALSE:
            self.eat(Token.TOKENTYPE.FALSE)
            return BooleanLiteral("false")
        elif token.type == Token.TOKENTYPE.LBRACK:
            return self.parse_array_literal()
        elif token.type == Token.TOKENTYPE.NAME:
            # Check if it's a function call
            lookahead_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if lookahead_token and lookahead_token.type == Token.TOKENTYPE.LPAREN:
                return self.parse_function_call()
            elif lookahead_token and lookahead_token.type == Token.TOKENTYPE.DOT:
                return self.parse_method_call(Variable(token.value))
            else:
                self.eat(Token.TOKENTYPE.NAME)
                return Variable(token.value)
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
        return IfStatement(condition, if_body, else_body)
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
        return WhileStatement(condition, body)

def parse_program(tokens):
    parser = Parser(tokens)
    return parser.parse()

def simple_ast_format(ast):
    # This function is used to format the AST for printing

    def format_node(node, indent=0):
        if isinstance(node, list):
            return "".join([format_node(item, indent) for item in node])
        elif isinstance(node, dict):
            string = ""
            for key, value in node.items():
                string += "\t" * indent + str(key) + "\n"
                string += format_node(value, indent + 1)
            return string
        else:
            return "\t" * indent + str(node) + "\n"
    return format_node(ast)


def parse_program(tokens):
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    import Lexer, json
    program =  """
    var x = [1,2,3,4,5,6,7,8,9,10]
    print(x.sort())

    """
    tokens = Lexer.tokenize(program)
    print(tokens)
    print(simple_ast_format(parse_program(tokens)))
