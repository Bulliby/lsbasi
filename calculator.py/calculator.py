#!/usr/bin/python

class Token():
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return 'This object is a Token of the type {type}  with value {value}'.format(type=self.token, value=self.value)

class Lexer():
    def __init__(self, userInput):
        self.userInput = userInput
        self.pos = 0
        self.len = len(self.userInput)

    def __str__(self):
        return "This object transform the user input in Lexems"

    def currentChar(self):
        return self.userInput[self.pos]

    def advance(self):
        self.pos += 1

    def splitInput(self):
        tokens = []
        while self.pos < self.len:
            if self.currentChar().isdigit():
                tokens.append(Token('INT', self.handleInteger()))
            elif self.currentChar() == '+':
                tokens.append(Token('PLUS', self.handleOperator()))
            elif self.currentChar() == '-':
                tokens.append(Token('MINUS', self.handleOperator()))
            elif self.currentChar() == '/':
                tokens.append(Token('DIV', self.handleOperator()))
            elif self.currentChar() == '*':
                tokens.append(Token('MUL', self.handleOperator()))
            else:
                raise Exception("Invalid Character")
        tokens.append(Token(None, 0))
        return tokens

    def handleInteger(self):
        integer = ""
        while self.pos < self.len and self.currentChar().isdigit():
            integer += self.currentChar()
            self.advance()
        return integer

    def handleOperator(self):
        operator = self.currentChar()
        self.advance()
        return operator

    def handleWhiteSpace(self):
        while self.currentChar().isspace():
            self.advance()

class BinOp():
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

    def __str__(self):
        return "Opérateur binaire {operator} avec left : {left} et right : {right}".format(operator=self.operator, left=self.left, right=self.right)

class Int():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Interger who's value is {value}".format(value=self.value)

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.nbTokens = len(tokens)

    def __str__(self):
        return 'This object handle the parsing of the expression'

    def getToken(self):
        return self.tokens[self.pos]

    def getNextToken(self):
        self.pos+=1

    def eat(self, token, value):
        if token.token != value:
            raise Exception("Parse Error")
        self.getNextToken()

    def exp(self):
        node = self.term()
        while self.getToken().token == 'PLUS' or self.getToken().token == 'MINUS':
            token = self.getToken().token 
            if self.getToken().token == 'PLUS':
                self.eat(self.getToken(), 'PLUS')
            elif self.getToken().token == 'MINUS':
                self.eat(self.getToken(), 'MINUS')
            node = BinOp(node, self.term(), token)
        return node


    def term(self):
        node = self.factor()
        while self.getToken().token == 'MUL' or self.getToken().token == 'DIV':
            token = self.getToken().token
            if self.getToken().token == 'MUL':
                self.eat(self.getToken(), 'MUL')
            elif self.getToken().token == 'DIV':
                self.eat(self.getToken(), 'DIV')
            node = BinOp(node, self.factor(), token)
        return node

    def factor(self):
        integer = self.getToken().value
        self.eat(self.getToken(), 'INT')
        return Int(int(integer))

    def parse(self):
        return self.exp()

class Interpreter():
    def __init__(self, root):
        self.root = root
        self.total = 0

    def visitNode(self, node):
        if type(node) is not Int:
            self.visitNode(node.left)
            self.visitNode(node.right)
            print(node)

input = input()
lexer = Lexer(input)
tokens = lexer.splitInput()
parser = Parser(tokens)
nodes = parser.parse()

interpreter = Interpreter(nodes)
interpreter.visitNode(nodes)
