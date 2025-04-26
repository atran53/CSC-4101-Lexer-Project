class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.current_token = self.tokens[self.current]

    def eat(self, token_type=None, token_value=None):
        if token_type and self.current_token.type != token_type:
            self.error(f"Expected token type {token_type}, got {self.current_token.type}")
        if token_value and self.current_token.value != token_value:
            self.error(f"Expected token value {token_value}, got {self.current_token.value}")
        self.advance()

    def advance(self):
        self.current += 1
        if self.current < len(self.tokens):
            self.current_token = self.tokens[self.current]
        else:
            self.current_token = None

    def error(self, message):
        raise Exception(f"Parse error: {message}")

    def parse_program(self):
        self.eat(token_value='program')
        self.parse_statements()
        self.eat(token_value='end_program')

    def parse_statements(self):
        while self.current_token.value not in ('end_program', 'end_if', 'end_loop', None):
            self.parse_statement()

    def parse_statement(self):
        if self.current_token.type == 'IDENTIFIER':
            self.parse_assignment()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'loop':
            self.parse_loop()
        elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
            self.parse_if_statement()
        else:
            self.error(f"Unexpected statement starting with {self.current_token}")

    def parse_assignment(self):
        self.eat(token_type='IDENTIFIER')
        self.eat(token_value='=')
        self.parse_expression()
        self.eat(token_value=';')

    def parse_expression(self):
        self.parse_term()
        while self.current_token is not None and self.current_token.value in ('+', '-'):
            self.eat(token_value=self.current_token.value)
            self.parse_term()

    def parse_term(self):
        self.parse_factor()
        while self.current_token is not None and self.current_token.value in ('*', '/', '%'):
            self.eat(token_value=self.current_token.value)
            self.parse_factor()

    def parse_factor(self):
        if self.current_token.type == 'IDENTIFIER':
            self.eat(token_type='IDENTIFIER')
        elif self.current_token.type == 'NUMBER':
            self.eat(token_type='NUMBER')
        elif self.current_token.value == '(':
            self.eat(token_value='(')
            self.parse_expression()
            self.eat(token_value=')')
        else:
            self.error(f"Unexpected factor: {self.current_token}")
    
    def parse_loop(self):
        """
        Grammar:
        <loop> ::= 'loop' '(' <identifier> '=' <expression> ':' <expression> ')' <statements> 'end_loop'
        """
        self.eat(token_value='loop')         # Match 'loop'
        self.eat(token_value='(')             # Match '('
        self.eat(token_type='IDENTIFIER')     # Match loop variable (identifier)
        self.eat(token_value='=')             # Match '='
        self.parse_expression()               # Match starting expression (e.g., 0)
        self.eat(token_value=':')              # Match ':'
        self.parse_expression()               # Match ending expression (e.g., 10)
        self.eat(token_value=')')              # Match ')'
        self.parse_statements()                # Parse loop body
        self.eat(token_value='end_loop')       # Match 'end_loop'

    def parse_if_statement(self):
        self.eat(token_value='if')
        self.eat(token_value='(')
        self.parse_logic_expression()
        self.eat(token_value=')')
        self.parse_statements()
        self.eat(token_value='end_if')

    def parse_logic_expression(self):
        self.parse_relation()
        while self.current_token is not None and self.current_token.value in ('&&', '||'):
            self.eat(token_value=self.current_token.value)
            self.parse_relation()

    def parse_relation(self):
        self.eat(token_type='IDENTIFIER')
        if self.current_token.value in ('==', '!=', '>', '<', '>=', '<='):
            self.eat(token_value=self.current_token.value)
        else:
            self.error(f"Expected a relational operator, got {self.current_token}")
        self.eat(token_type='IDENTIFIER')
