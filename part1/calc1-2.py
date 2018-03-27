INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if (self.pos > len(self.text) - 1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skipeWs(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def integer(self):
        digits = ""
        while self.current_char and self.current_char.isdigit():
            digits += self.current_char
            self.advance()
        return int(digits)

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):

        self.skipeWs()

        if self.current_char == None:
            token = Token(EOF, None)
            return token

        if self.current_char.isdigit():
            token = Token(INTEGER, self.integer())
            return token

        if self.current_char == '-':
            token = Token(MINUS, self.current_char)
            self.advance()
            return token

        if self.current_char == '+':
            token = Token(PLUS, self.current_char)
            self.advance()
            return token
        self.skipeWs()
        
        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value

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
