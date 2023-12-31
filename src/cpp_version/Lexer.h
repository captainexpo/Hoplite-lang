#ifndef LEXER_H
#define LEXER_H

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <regex>
#include "Tokens.h"


class Lexer {
private:
    std::string text;
    size_t pos;
    char current_char;
    std::vector<Token> tokens;
    std::map<TOKENTYPE, std::regex> token_rules;
    std::vector<TOKENTYPE> token_priority;

public:
    Lexer(const std::string& text) : text(text), pos(0), current_char(text[0]) {
        token_rules = TOKEN_RULES;
        token_priority = TOKEN_PRIORITY;
    }

    void error(char character) {
        throw std::runtime_error("Invalid character: " + std::string(1, character));
    }

    void advance() {
        pos++;
        if (pos > text.size() - 1) {
            current_char = '\0'; // Using '\0' to denote end of text
        } else {
            current_char = text[pos];
        }
    }

    void skip_whitespace() {
        while (current_char != '\0' && isspace(current_char)) {
            advance();
        }
    }

    Token get_next_token() {
        while (current_char != '\0') {
            for (auto token_type : token_priority) {
                std::smatch match;
                std::string substr = text.substr(pos);
                if (std::regex_search(substr, match, token_rules[token_type]) && match.position() == 0) {
                    pos += match.length();
                    current_char = pos < text.size() ? text[pos] : '\0';
                    if (!match.str(0).empty()) {
                        return Token(token_type, match.str(0));
                    }
                }
            }
            error(current_char);
        }
        return Token(TOKENTYPE::EOF_TOKEN, "");
    }

    std::vector<Token> tokenize() {
        while (current_char != '\0') {
            skip_whitespace();
            Token next_token = get_next_token();
            tokens.push_back(next_token);
            if (next_token.type == TOKENTYPE::EOF_TOKEN) {
                break;
            }
        }
        return tokens;
    }
};


std::vector<Token> tokenize(const std::string& text) {
    Lexer lexer(text);
    return lexer.tokenize();
}

#endif