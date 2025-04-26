import re
# Define the token types

class TokenType:
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    SYMBOL = 'SYMBOL'
    EOF = 'EOF'  # EOF = End of File (I'm going to forget this name lol)

# Define token class

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"
    
# Define the Lexer
class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []
        self.keywords = {'program', 'end_program', 'if', 'end_if', 'loop' 'end_loop'}

        # Define the token specifications
        self.token_specification = [
            ('NUMBER',   r'\d+'),           # Integer
            ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
            ('SYMBOL', r'==|!=|>=|<=|&&|\|\||=|\+|-|\*|/|%|\(|\)|;|:|>|<'), # Operators and punctuations
            ('NEWLINE', r'\n'), # Newline
            ('SKIP', r'[ \t]+'), # Skip spaces and tabs
            ('COMMENT', r'//.*'), # Skip comments starting with //
            ('MISMATCH', r'.') # Anything else is considered a mismatch
        ]
    def tokenize(self):
        # Combines all token types into one single regex pattern
        tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in self.token_specification)
        for mo in re.finditer(tok_regex, self.source): 
            kind = mo.lastgroup     
            value = mo.group()      
            if kind == 'NUMBER':
                self.tokens.append(Token(TokenType.NUMBER, int(value)))
            elif kind == 'IDENTIFIER':
                if value in self.keywords:
                    self.tokens.append(Token(TokenType.KEYWORD, value))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, value))
            elif kind == 'SYMBOL':
                self.tokens.append(Token(TokenType.SYMBOL, value))
            elif kind == 'NEWLINE' or kind == 'SKIP' or kind == 'COMMENT':
                continue  
            elif kind == 'MISMATCH':
                raise RuntimeError(f"Unexpected character {value}")

        self.tokens.append(Token(TokenType.EOF, None))  # End of file
        return self.tokens