from token import Token


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []

    def scan_tokens(self):
        while self.pos < len(self.text):
            self.scan_token()

        # add special token to indicate end of file
        self.add_token(Token("EOF"))

        return self.tokens


    def scan_token(self):
        # inside armadillo code
        if self.current() == '{' and self.peek() == '{':
            # skip opening brackets
            self.pos += 2

            while not (self.current() == '}' and self.peek() == '}'):
                # get next character
                c = self.advance()

                match c:
                    # required
                    case "!": self.add_token(Token("REQUIRED"))
                
                    # keyword token
                    case "#":
                        value = ""
                        while self.current() not in [' ', '}']:
                            value += self.advance()

                        keyword_token = self.keyword(value)
                        self.add_token(keyword_token)

                    # extension token
                    case ":":
                        value = ""
                        while self.current() not in [' ', '}', ':']:
                            value += self.advance()

                        extension_token = self.extension(value)
                        self.add_token(extension_token)

                    # skip whitespace
                    case " ": continue

                    # variable or parent
                    case _: self.add_token(self.variable(c))

            # skip closing brackets
            self.pos += 2
        else:
            # html token
            self.add_token(Token("HTML", self.advance()))


    def keyword(self, value):
        match value:
            case "foreach":
                return Token("FOREACH")
            case "end":
                return Token("END")
            case "import":
                return Token("IMPORT")
            case _:
                return Token("ERROR", f"Keyword {value} not found.")


    def extension(self, value):
        if value in ["upper", "lower", "quotes", "single-quotes", "double-quotes", "escape"]:
            return Token("EXTENSION", value)
        else:
            return Token("ERROR", f"Extension type {value} not found")


    def variable(self, start_c):
        value = start_c
        while self.current() not in [' ', '}', ':']:
            c = self.advance()
            if c == '.':
                return Token("PARENT", value)

            value += c
        return Token("VAR", value)


    def peek(self):
        return self.text[self.pos+1]


    def advance(self):
        value = self.current()
        self.pos += 1
        return value


    def current(self):
        return self.text[self.pos]


    def add_token(self, token):
        self.tokens.append(token)
