PLUS, MINUS, MUL, DIV, INTEGER, LPAREN, RPAREN, EOF = 'PLUS', 'MINUS', 'MUL', 'DIV', 'INTEGER', 'LPAREN', 'RPAREN', 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.pos = 0
        self.text = text
        self.current_char = self.text[self.pos]

    def advance(self):
        if (self.pos < len(self.text) - 1):
            self.pos += 1
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def integer(self):
        ret = ''
        while self.current_char and self.current_char.isdigit():
            ret += self.current_char
            self.advance()
        return int(ret)

    def whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def error(self):
        raise Exception ('Invalid Token')
            
    def get_next_token(self):
        while self.current_char:

            if self.current_char.isspace():
                self.whitespace()
                continue
            
            if self.current_char.isdigit():
                value = self.integer()
                return Token(INTEGER, value)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)

class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.result = 0

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.lexer.error()

    def factor(self):
        if self.current_token.type == INTEGER:
            value = self.current_token.value
            self.eat(INTEGER)
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            value = self.expr()
            self.eat(RPAREN)
        return value

    def term(self):
        self.result = self.factor()
        while self.current_token.type in (MUL, DIV):
            if self.current_token.type == DIV:
                self.eat(DIV)
                self.result /= self.factor()
            elif self.current_token.type == MUL:
                self.eat(MUL)
                self.result *= self.factor()
        return self.result
        
    def expr(self):
        self.result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                self.result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                self.result -= self.term()

        return self.result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
