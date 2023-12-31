

#include "ParserClass.h"
#include "Lexer.h"

// Constructor implementation
Parser::Parser(const std::vector<Token>& tokens) : tokens(tokens), pos(0) {}

// Implementations of other methods
void Parser::error(const std::string& message) {
    throw std::runtime_error(message);
}

Token Parser::current_token() {
    if (pos < tokens.size()) {
        return tokens[pos];
    }
    return Token(TOKENTYPE::EOF_TOKEN, "");
}

void Parser::eat(TOKENTYPE token_type) {
    if (current_token().type == token_type) {
        pos++;
    } else {
        error("Expected token: " + TOKENTYPE_to_string(token_type) + ", found: " + TOKENTYPE_to_string(current_token().type) + " at: " + std::to_string(pos));
    }
}

Statement* Parser::get_statement() {
    if (current_token().type == TOKENTYPE::VAR) {
        return parse_variable_declaration();
    } else if (current_token().type == TOKENTYPE::RETURN) {
        return parse_return_statement();
    } else if (current_token().type == TOKENTYPE::IF) {
        return parse_if_statement();
    } else if (current_token().type == TOKENTYPE::WHILE) {
        return parse_while_statement();
    } else if (current_token().type == TOKENTYPE::FUNCTION_DECLARATION) {
        return parse_function_declaration();
    } else {
        return parse_expression_statement();
    }
}

Statement* Parser::parse_variable_declaration() {
    eat(TOKENTYPE::VAR);
    std::string variable_name = current_token().value;
    eat(TOKENTYPE::NAME);
    eat(TOKENTYPE::EQUALS);
    Expression* expr = parse_expression();
    return new VariableDeclaration(variable_name, expr);
}

Statement* Parser::parse_return_statement() {
    eat(TOKENTYPE::RETURN);
    Expression* expr = parse_expression();
    return new ReturnStatement(expr);
}

Statement* Parser::parse_expression_statement() {
    Expression* expr = parse_expression();
    return new ExpressionStatement(expr);
}

std::vector<std::string> Parser::parse_parameters() {
    std::vector<std::string> parameters;
    eat(TOKENTYPE::LPAREN);
    if (current_token().type == TOKENTYPE::RPAREN) {
        eat(TOKENTYPE::RPAREN);
        return parameters;
    }
    parameters.push_back(current_token().value);
    eat(TOKENTYPE::NAME);
    while (current_token().type == TOKENTYPE::COMMA) {
        eat(TOKENTYPE::COMMA);
        parameters.push_back(current_token().value);
        eat(TOKENTYPE::NAME);
    }
    eat(TOKENTYPE::RPAREN);
    return parameters;
}

Block* Parser::parse_block() {
    eat(TOKENTYPE::LBRACE);
    std::vector<Statement*> statements;
    while (current_token().type != TOKENTYPE::RBRACE) {
        statements.push_back(get_statement());
    }
    eat(TOKENTYPE::RBRACE);
    return new Block(statements);
}

Statement* Parser::parse_if_statement() {
    eat(TOKENTYPE::IF);
    Expression* condition = parse_expression();
    Block* if_block = parse_block();
    Block* else_block = nullptr;
    if (current_token().type == TOKENTYPE::ELSE) {
        else_block = parse_else_statement();
    }
    return new IfStatement(condition, if_block, else_block);
}

Block* Parser::parse_else_statement() {
    eat(TOKENTYPE::ELSE);
    return parse_block();
}

Expression* Parser::parse_atom(){

    Token token = current_token();
    if (token.type == TOKENTYPE::INTEGER) {
        eat(TOKENTYPE::INTEGER);
        return new NumberLiteral("int", token.value);
    } else if (token.type == TOKENTYPE::FLOAT) {
        eat(TOKENTYPE::FLOAT);
        return new NumberLiteral("float", token.value);
    } else if (token.type == TOKENTYPE::STRING) {
        eat(TOKENTYPE::STRING);
        return new StringLiteral(token.value);
    } else if (token.type == TOKENTYPE::TRUE) {
        eat(TOKENTYPE::TRUE);
        return new BooleanLiteral(true);
    } else if (token.type == TOKENTYPE::FALSE) {
        eat(TOKENTYPE::FALSE);
        return new BooleanLiteral(false);
    } else if (token.type == TOKENTYPE::NAME) {
        eat(TOKENTYPE::NAME);
        return new Variable(token.value);
    } else if (token.type == TOKENTYPE::LPAREN) {
        eat(TOKENTYPE::LPAREN);
        Expression* expr = parse_expression();
        eat(TOKENTYPE::RPAREN);
        return expr;
    }
}   

Expression* Parser::parse_factor(){
    /*Python example
    def parse_factor(self):
        node = self.parse_atom()

        while self.current_token() is not None and self.current_token().type in (Token.TOKENTYPE.MUL, Token.TOKENTYPE.DIV):
            token_type = self.current_token().type
            self.eat(token_type)
            node = BinaryOperation(node, token_type, self.parse_atom())

        return node
    */

    Expression* expr = parse_atom();
    while (current_token().type == TOKENTYPE::MUL || current_token().type == TOKENTYPE::DIV) {
        if (current_token().type == TOKENTYPE::MUL) {
            eat(TOKENTYPE::MUL);
            expr = new BinaryOperation(expr, TOKENTYPE::MUL, parse_atom());
        } else if (current_token().type == TOKENTYPE::DIV) {
            eat(TOKENTYPE::DIV);
            expr = new BinaryOperation(expr, TOKENTYPE::DIV , parse_atom());

        }
    }
    return expr;
}

Statement* Parser::parse_while_statement() {
    eat(TOKENTYPE::WHILE);
    Expression* condition = parse_expression();
    Block* while_block = parse_block();
    return new WhileStatement(condition, while_block);
}

FunctionDeclaration* Parser::parse_function_declaration() {
    eat(TOKENTYPE::FUNCTION_DECLARATION);
    std::string name = current_token().value;
    eat(TOKENTYPE::NAME);
    std::vector<std::string> parameters = parse_parameters();
    Block* body = parse_block();
    return new FunctionDeclaration(name, parameters, body);
}

FunctionCall* Parser::parse_function_call() {
    std::string name = current_token().value;
    eat(TOKENTYPE::NAME);
    eat(TOKENTYPE::LPAREN);
    std::vector<Expression*> arguments = parse_arguments();
    eat(TOKENTYPE::RPAREN);
    return new FunctionCall(name, arguments);
}

std::vector<Expression*> Parser::parse_arguments() {
    std::vector<Expression*> arguments;
    while (current_token().type != TOKENTYPE::RPAREN) {
        std::cout << arguments.size() << std::endl;
        arguments.push_back(parse_expression());
        if (current_token().type == TOKENTYPE::COMMA) {
            eat(TOKENTYPE::COMMA);
        }
        else if (current_token().type == TOKENTYPE::RPAREN) {
            break;
        }
    }
    std::cout << arguments.size() << std::endl;
    return arguments;
}


Expression* Parser::parse_expression() {
    Expression* expr = parse_term();
    while (current_token().type == TOKENTYPE::IS_EQUAL ||
           current_token().type == TOKENTYPE::LESS_THAN ||
           current_token().type == TOKENTYPE::GREATER_THAN ||
           current_token().type == TOKENTYPE::LESS_THAN_OR_EQUAL ||
           current_token().type == TOKENTYPE::GREATER_THAN_OR_EQUAL ||
           current_token().type == TOKENTYPE::NOT_EQUAL) {
        TOKENTYPE token_type = current_token().type;
        eat(token_type);
        expr = new ComparisonOperation(expr, token_type, parse_term());
    }
    return expr;
}

Expression* Parser::parse_term() {
    Expression* expr = parse_factor();
    while (current_token().type == TOKENTYPE::MUL || current_token().type == TOKENTYPE::DIV) {
        if (current_token().type == TOKENTYPE::MUL) {
            eat(TOKENTYPE::MUL);
            expr = new BinaryOperation(expr, TOKENTYPE::MUL, parse_factor());
        } else if (current_token().type == TOKENTYPE::DIV) {
            eat(TOKENTYPE::DIV);
            expr = new BinaryOperation(expr, TOKENTYPE::DIV , parse_factor());
        }
        
    }
    return expr;
}

std::vector<Statement*> Parser::parse() {
    std::vector<Statement*> statements;
    while (current_token().type != TOKENTYPE::EOF_TOKEN) {
        statements.push_back(get_statement());
    }
    return statements;
}

int main(){
    std::string program = R"(
        var a = 5
        mkfunc add(a, b) {
            return a + b
        }
        var b = add(5, 10)
        print(b)
    )";
    Lexer lexer(program);
    std::vector<Token> tokens = lexer.tokenize();
    for (auto token : tokens) {
        std::cout << token.toString() << std::endl;
    }

    Parser parser(tokens);
    std::vector<Statement*> statements = parser.parse();
    for (auto statement : statements) {
        std::cout << statement->toString() << std::endl;
    }
}
