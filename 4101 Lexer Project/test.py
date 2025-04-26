from lexer import Lexer
from parser import Parser

# Step 1: Example program
source_code = """
program
x = 5;
y = 10;
if (x < y)
    x = x + 1;
end_if
end_program
"""

# Step 2: Tokenize
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# Show the tokens
print("Tokens:")
for token in tokens:
    print(token)

# Step 3: Parse
parser = Parser(tokens)

try:
    parser.parse_program()
    print("Parsing successful! 🎉")
except Exception as e:
    print(e)
