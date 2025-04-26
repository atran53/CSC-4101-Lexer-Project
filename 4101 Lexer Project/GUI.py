import tkinter as tk
from lexer import Lexer
from parser import Parser

class ParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexer and Parser GUI")

        # Text box for inputting source code
        self.text_box = tk.Text(root, height=20, width=80)
        self.text_box.pack(padx=10, pady=10)

        # Parse button
        self.parse_button = tk.Button(root, text="Parse", command=self.parse_code)
        self.parse_button.pack(pady=5)

        # Label for showing result (success or error)
        self.result_label = tk.Label(root, text="", fg="green")
        self.result_label.pack(pady=5)

        # NEW: Text box for showing tokens
        self.tokens_box = tk.Text(root, height=10, width=80, state='disabled')
        self.tokens_box.pack(padx=10, pady=10)

    def parse_code(self):
        # Clear the tokens box
        self.tokens_box.config(state='normal')
        self.tokens_box.delete("1.0", tk.END)

        # Get the text entered in the Text box
        source_code = self.text_box.get("1.0", tk.END)

        # Create a Lexer and tokenize the source code
        lexer = Lexer(source_code)
        try:
            tokens = lexer.tokenize()

            # Create a Parser using the tokens
            parser = Parser(tokens)

            # Parse the entire program
            parser.parse_program()

            # If no errors, show success message
            self.result_label.config(text="Parsing successful!", fg="green")

            # Display the tokens
            for token in tokens:
                self.tokens_box.insert(tk.END, f"{token}\n")

            self.tokens_box.config(state='disabled')  # Make it read-only again

        except Exception as e:
            # If an error happens, show the error message
            self.result_label.config(text=str(e), fg="red")
            self.tokens_box.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ParserGUI(root)
    root.mainloop()
