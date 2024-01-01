import Tokens as token

class Lexer:
    def __init__(self, text=None):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.tokens = []
        self.token_rules = token.TOKEN_RULES
        self.token_priority = token.TOKEN_PRIORITY

    def error(self, character=''):
        raise Exception("Invalid character: " + character)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            for token_type in self.token_priority:
                match = self.token_rules[token_type].match(self.text, self.pos)
                if match:
                    self.pos = match.end()
                    if self.pos >= len(self.text):  # Check to prevent index out of range
                        self.current_char = None
                    else:
                        self.current_char = self.text[self.pos]
                    if match.group(0) is not None:
                        return token.Token(token_type, match.group(0))
            self.error(self.current_char)

    def tokenize(self):
        while self.current_char is not None:
            self.skip_whitespace()
            NEXT = self.get_next_token()
            if NEXT:
                self.tokens.append(NEXT)
            else:
                self.tokens.append(token.Token(token.TOKENTYPE.EOF, ""))
            #print(self.tokens)
        return self.tokens
    
def tokenize(text):
    lexer = Lexer(text)
    return lexer.tokenize()

if __name__ == "__main__":
    print(
        tokenize(
            """for(var i = 0, i < 10, i += 1) {
                print(i)
            }"""
        )
    )