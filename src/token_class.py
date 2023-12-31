import re

class TOKENTYPE:
    LBRACK = "LBRACK"
    RBRACK = "RBRACK"
    COMMENT = "COMMENT"
    QUOTE = "QUOTE"
    STRING = "STRING"
    SINGLE_QUOTE = "SINGLE_QUOTE"
    MODULO = "MODULO"
    CARAT = "CARAT"
    BANG = "BANG"
    ELSE = "ELSE"
    WHILE = "WHILE"
    IF = "IF"
    TRUE = "TRUE"
    FALSE = "FALSE"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    IS_EQUAL = "IS_EQUAL"
    RETURN = "RETURN"
    RBRACE = "RBRACE"
    LBRACE = "LBRACE"
    COMMA = "COMMA"
    FUNCTION_DECLARATION = "FUNCTION_DECLARATION"
    SEMICOLON = "SEMICOLON"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    NAME = "NAME"
    VAR = "VAR"
    DOT = "DOT"
    EQUALS = "EQUALS"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"

TOKEN_RULES = {
    TOKENTYPE.LBRACK: r"\[",
    TOKENTYPE.RBRACK: r"\]",
    TOKENTYPE.COMMENT: r"\/\/.*",
    TOKENTYPE.STRING: r"\"[^\"]*\"",
    TOKENTYPE.QUOTE: r"\"",
    TOKENTYPE.SINGLE_QUOTE: r"\'",
    TOKENTYPE.MODULO: r"%",
    TOKENTYPE.CARAT: r"\^",
    TOKENTYPE.BANG: r"!",
    TOKENTYPE.ELSE: r"else",
    TOKENTYPE.WHILE: r"while",
    TOKENTYPE.IF: r"if",
    TOKENTYPE.TRUE : r"true",
    TOKENTYPE.FALSE: r"false",
    TOKENTYPE.GREATER_THAN: r">",
    TOKENTYPE.LESS_THAN: r"<",
    TOKENTYPE.LESS_THAN_OR_EQUAL: r"<=",
    TOKENTYPE.GREATER_THAN_OR_EQUAL: r">=",
    TOKENTYPE.IS_EQUAL: r"==",
    TOKENTYPE.RETURN: r"return",
    TOKENTYPE.COMMA: r",",
    TOKENTYPE.FUNCTION_DECLARATION: r"mkfunc",
    TOKENTYPE.SEMICOLON: r";",
    TOKENTYPE.INTEGER: r"( -)?(\d+)",
    TOKENTYPE.FLOAT: r"-?(\d+\.\d+)",
    TOKENTYPE.LPAREN: r"\(",
    TOKENTYPE.RPAREN: r"\)",
    TOKENTYPE.LBRACE: r"\{",
    TOKENTYPE.RBRACE: r"\}",
    TOKENTYPE.NAME: r"[a-zA-Z_][a-zA-Z0-9_]*",
    TOKENTYPE.VAR: r"var",
    TOKENTYPE.EQUALS: r"=",
    TOKENTYPE.PLUS: r"\+",
    TOKENTYPE.MINUS: r"-",
    TOKENTYPE.MUL: r"\*",
    TOKENTYPE.DIV: r"/",
    TOKENTYPE.DOT: r"\."
}
# which tokens should be checked for first. E.G. VAR should be before NAME
# in this list, index zero is checked first, then index one, etc.
TOKEN_PRIORITY = [
    # ----- special -----
    TOKENTYPE.COMMENT,
    # ----- data types -----
    TOKENTYPE.FLOAT,
    TOKENTYPE.INTEGER,
    TOKENTYPE.TRUE,
    TOKENTYPE.FALSE,
    TOKENTYPE.STRING,
    # ----- keywords -----
    TOKENTYPE.ELSE,
    TOKENTYPE.WHILE,
    TOKENTYPE.RETURN,
    TOKENTYPE.FUNCTION_DECLARATION,
    TOKENTYPE.VAR,
    TOKENTYPE.IF,
    # ----- symbols -----
    TOKENTYPE.COMMA,
    TOKENTYPE.BANG,
    TOKENTYPE.SEMICOLON,
    TOKENTYPE.LPAREN,
    TOKENTYPE.RPAREN,
    TOKENTYPE.LBRACE,
    TOKENTYPE.RBRACE,
    TOKENTYPE.LBRACK,
    TOKENTYPE.RBRACK,
    TOKENTYPE.SINGLE_QUOTE,
    TOKENTYPE.QUOTE,
    # ----- operators -----
    TOKENTYPE.MODULO,
    TOKENTYPE.CARAT,
    TOKENTYPE.LESS_THAN_OR_EQUAL,
    TOKENTYPE.GREATER_THAN_OR_EQUAL,
    TOKENTYPE.LESS_THAN,
    TOKENTYPE.GREATER_THAN,
    TOKENTYPE.IS_EQUAL,
    TOKENTYPE.EQUALS,
    TOKENTYPE.PLUS,
    TOKENTYPE.MINUS,
    TOKENTYPE.MUL,
    TOKENTYPE.DIV,
    TOKENTYPE.DOT,
    # ----- identifier -----
    TOKENTYPE.NAME
]

for key, value in TOKEN_RULES.items():
    TOKEN_RULES[key] = re.compile(value)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, \"{self.value}\")"
    
    def __str__(self):
        return self.__repr__()