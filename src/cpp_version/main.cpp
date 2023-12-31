#include "Lexer.h"



int main(){
    Lexer lexer("var x = 5;");
    std::vector<Token> tokens = lexer.tokenize();
    for (auto token : tokens) {
        std::cout << token.toString() << std::endl;
    }

}