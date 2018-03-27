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

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if (self.pos > len(self.text) - 1):
            self.current_char = None
        else
            self.current_char = self.text[self.pos]

    def discardWhiteSpace(self):
        current_char = self.text[self.pos]
        while current_char.isspace() and self.pos < len(self.text):
            self.pos+=1
            if self.pos < len(self.text):
                current_char = self.text[self.pos]

    def get_next_token(self):
        text = self.text

        if self.pos > len(self.text) - 1:
            return Token(EOF, None)
        self.discardWhiteSpace()
        if self.pos > len(self.text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]
        if current_char.isdigit():
            digits = ""
            while current_char.isdigit() and self.pos < len(text):
                digits += current_char
                self.pos += 1
                if self.pos < len(text):
                    current_char = text[self.pos]
            token = Token(INTEGER, int(digits))
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

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
        self.eat(PLUS)

        right = self.current_token
        self.eat(INTEGER)
        result = left.value + right.value
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
