#ifndef PARSER_H
#define PARSER_H

#include <string>
#include <vector>
#include <stdexcept>
#include "ParserTypes.h"    // Assuming necessary parser type definitions are in this header

class Parser {
private:
    std::vector<Token> tokens;
    size_t pos;

public:
    Parser(const std::vector<Token>& tokens);

    void error(const std::string& message = "Invalid syntax");
    Token current_token();
    void eat(TOKENTYPE token_type);

    // Declare other member functions
    Statement* get_statement();
    Statement* parse_variable_declaration();
    Statement* parse_return_statement();
    Statement* parse_expression_statement();
    std::vector<std::string> parse_parameters();
    Block* parse_block();
    Statement* parse_if_statement();
    Block* parse_else_statement();
    Statement* parse_while_statement();
    FunctionDeclaration* parse_function_declaration();
    FunctionCall* parse_function_call();
    std::vector<Expression*> parse_arguments();
    Expression* parse_expression();
    Expression* parse_term();
    Expression* parse_factor();
    Expression* parse_atom();

    std::vector<Statement*> parse();
};

#endif // PARSER_H