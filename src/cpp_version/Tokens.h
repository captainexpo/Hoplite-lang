#ifndef TOKENS_H
#define TOKENS_H


#include <iostream>
#include <string>
#include <regex>
#include <map>
#include <vector>

enum class TOKENTYPE {
    EOF_TOKEN, NOT_EQUAL, LBRACK, RBRACK, COMMENT, QUOTE, STRING, SINGLE_QUOTE,
    MODULO, CARAT, BANG, ELSE, WHILE, IF, TRUE, FALSE, GREATER_THAN, LESS_THAN,
    LESS_THAN_OR_EQUAL, GREATER_THAN_OR_EQUAL, IS_EQUAL, RETURN, RBRACE, LBRACE,
    COMMA, FUNCTION_DECLARATION, SEMICOLON, INTEGER, FLOAT, LPAREN, RPAREN, NAME, VAR,
    DOT, EQUALS, PLUS, MINUS, MUL, DIV
};

std::map<TOKENTYPE, std::regex> TOKEN_RULES = {
    {TOKENTYPE::EOF_TOKEN, std::regex("^$")},
    {TOKENTYPE::COMMENT, std::regex("^#.*")},
    {TOKENTYPE::FLOAT, std::regex("^\\d+\\.\\d+")},
    {TOKENTYPE::INTEGER, std::regex("^\\d+")},
    {TOKENTYPE::TRUE, std::regex("^true")},
    {TOKENTYPE::FALSE, std::regex("^false")},
    {TOKENTYPE::STRING, std::regex("^\".*\"")},
    {TOKENTYPE::ELSE, std::regex("^else")},
    {TOKENTYPE::WHILE, std::regex("^while")},
    {TOKENTYPE::RETURN, std::regex("^return")},
    {TOKENTYPE::FUNCTION_DECLARATION, std::regex("^mkfunc")},
    {TOKENTYPE::VAR, std::regex("^var")},
    {TOKENTYPE::IF, std::regex("^if")},
    {TOKENTYPE::COMMA, std::regex("^,")},
    {TOKENTYPE::BANG, std::regex("^!")},
    {TOKENTYPE::SEMICOLON, std::regex("^;")},
    {TOKENTYPE::LPAREN, std::regex("^\\(")},
    {TOKENTYPE::RPAREN, std::regex("^\\)")},
    {TOKENTYPE::LBRACE, std::regex("^\\{")},
    {TOKENTYPE::RBRACE, std::regex("^\\}")},
    {TOKENTYPE::LBRACK, std::regex("^\\[")},
    {TOKENTYPE::RBRACK, std::regex("^\\]")},
    {TOKENTYPE::SINGLE_QUOTE, std::regex("^'")},
    {TOKENTYPE::QUOTE, std::regex("^\"")},
    {TOKENTYPE::MODULO, std::regex("^%")},
    {TOKENTYPE::CARAT, std::regex("^\\^")},
    {TOKENTYPE::NOT_EQUAL, std::regex("^!=")},
    {TOKENTYPE::LESS_THAN_OR_EQUAL, std::regex("^<=")},
    {TOKENTYPE::GREATER_THAN_OR_EQUAL, std::regex("^>=")},
    {TOKENTYPE::LESS_THAN, std::regex("^<")},
    {TOKENTYPE::GREATER_THAN, std::regex("^>")},
    {TOKENTYPE::IS_EQUAL, std::regex("^==")},
    {TOKENTYPE::EQUALS, std::regex("^=")},
    {TOKENTYPE::PLUS, std::regex("^\\+")},
    {TOKENTYPE::MINUS, std::regex("^-")},
    {TOKENTYPE::MUL, std::regex("^\\*")},
    {TOKENTYPE::DIV, std::regex("^/")},
    {TOKENTYPE::DOT, std::regex("^\\.")},
    {TOKENTYPE::NAME, std::regex("^[a-zA-Z_][a-zA-Z0-9_]*")}
};

std::vector<TOKENTYPE> TOKEN_PRIORITY = {
    TOKENTYPE::EOF_TOKEN, 
    TOKENTYPE::COMMENT, 
    TOKENTYPE::FLOAT, 
    TOKENTYPE::INTEGER, 
    TOKENTYPE::TRUE, 
    TOKENTYPE::FALSE, 
    TOKENTYPE::STRING, 
    TOKENTYPE::ELSE, 
    TOKENTYPE::WHILE,
    TOKENTYPE::RETURN, 
    TOKENTYPE::FUNCTION_DECLARATION, 
    TOKENTYPE::VAR,
    TOKENTYPE::IF, 
    TOKENTYPE::COMMA, 
    TOKENTYPE::BANG, 
    TOKENTYPE::SEMICOLON, 
    TOKENTYPE::LPAREN,
    TOKENTYPE::RPAREN, 
    TOKENTYPE::LBRACE, 
    TOKENTYPE::RBRACE, 
    TOKENTYPE::LBRACK, 
    TOKENTYPE::RBRACK, 
    TOKENTYPE::SINGLE_QUOTE, 
    TOKENTYPE::QUOTE, 
    TOKENTYPE::MODULO, 
    TOKENTYPE::CARAT,
    TOKENTYPE::NOT_EQUAL, 
    TOKENTYPE::LESS_THAN_OR_EQUAL, 
    TOKENTYPE::GREATER_THAN_OR_EQUAL, 
    TOKENTYPE::LESS_THAN, 
    TOKENTYPE::GREATER_THAN,
    TOKENTYPE::IS_EQUAL, 
    TOKENTYPE::EQUALS, 
    TOKENTYPE::PLUS, 
    TOKENTYPE::MINUS, 
    TOKENTYPE::MUL, 
    TOKENTYPE::DIV, 
    TOKENTYPE::DOT, 
    TOKENTYPE::NAME
};


std::string TOKENTYPE_to_string(TOKENTYPE type){
    return std::to_string(static_cast<int>(type));
}


class Token {
public:
    TOKENTYPE type;
    std::string value;
    Token(TOKENTYPE type, const std::string& value) : type(type), value(value) {}

    std::string toString() const {
        std::cout << "Token(" << static_cast<int>(type) << ", " << value << ")" << std::endl;
        return "Token(" + std::to_string(static_cast<int>(type)) + ", " + value + ")";
    }
};

#endif