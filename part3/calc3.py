INTEGER, PLUS, MINUS, MULT, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EOF'

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error():
        raise Exception('Error parsing input')

    def advance(self):
        if self.pos < len(self.text) - 1:
            self.pos += 1
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def whiteSpace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        ret = ""
        while self.current_char is not None and  self.current_char.isdigit():
            ret += self.current_char
            self.advance()
        print(ret)
        return (int(ret))

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def get_next_token(self):
        if self.current_char == None:
            return Token(EOF, None)
        if self.current_char.isspace():
            self.whiteSpace()
        if self.current_char == None:
            return Token(EOF, None)
        if self.current_char.isdigit(): 
            return Token(INTEGER, self.integer())
        elif self.current_char == '+':
            self.advance()
            return Token(PLUS, None)
        elif self.current_char == '-':
            self.advance()
            return Token(MINUS, None)
        elif self.current_char == '/':
            self.advance()
            return Token(DIV, None)
        elif self.current_char == '*':
            self.advance()
            return Token(MULT, None)
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()
        result = self.current_token.value
        self.eat(INTEGER)
        while self.current_token.type != EOF:
            op = self.current_token.type    
            if op == PLUS:
                self.eat(PLUS)
            elif op == MINUS:
                self.eat(MINUS)
            elif op == DIV:
                self.eat(DIV)
            elif op == MULT:
                self.eat(MULT)
            
            new = self.current_token
            self.eat(INTEGER)
            if op == PLUS:
                result+= new.value
            elif op == MINUS:
                result-= new.value
            elif op == DIV:
                result/= new.value
            elif op == MULT:
                result*= new.value

        return result
        

def main():
    while True:
        try:
            try:
                text = raw_input('calc> ')
            except NameError:  # Python3
                text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
