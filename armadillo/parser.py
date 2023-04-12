from armadillo import grammar
from armadillo import extensions
from armadillo import nodes


class Parser:
    def __init__(self, tokens, symbol_table=None):
        self.tokens = tokens
        self.pos = 0
        self.syntax_tree = []
        self.symbol_table = symbol_table or {}
        self.global_scope = "global"


    def parse(self):
        while self.pos < len(self.tokens):
            self.parse_token()

        return self.syntax_tree, self.symbol_table


    def parse_token(self):
        token = self.advance()

        match token.type:
            # parse HTML token
            case 'HTML':
                html_block = nodes.HTML(token.value)
                self.syntax_tree.append(html_block)

            # parse variable
            case 'VAR':
                var = self.process_variable(token)
                self.syntax_tree.append(var)
                self.add_variable_to_symbol_table(var)               

            #parse for each loop
            case 'FOREACH': 
                foreach_block = self.process_foreach()
                self.syntax_tree.append(foreach_block)
                
            # skip any other tokens
            case _: pass


    def advance(self):
        token = self.current()
        self.pos += 1
        return token


    def current(self):
        return self.tokens[self.pos]


    def match_type(self, pos, type):
        return self.tokens[pos].type == type


    def add_variable_to_symbol_table(self, var):
        # process object variable
        if var.parent:
            assert var.parent in self.symbol_table, f"[Parser] Reference '{var.parent}' not found"

            if var.name not in self.symbol_table[var.parent]['values']:
                self.symbol_table[var.parent]['values'][var.name] = {"type": "Variable", "scope": "Local"}

        # process global variable
        else:
            if var.name in self.symbol_table:
                assert self.symbol_table[var.name]["type"] == "Variable", f"[Parser] Object '{var.name}' referenced without value"
            else:
                self.symbol_table[var.name] = {"type": "Variable", "scope": "Global"}


    def process_variable(self, token):
        var = nodes.Variable(token.value)
        ptr = self.pos-1

        # check for parents, requried, or foreach
        while True:
            ptr -= 1
            if ptr < 0: break
            elif self.match_type(ptr, grammar.PARENT): var.parent = self.tokens[ptr].value
            elif self.match_type(ptr, grammar.REQUIRED): var.required = True
            elif self.match_type(ptr, grammar.FOREACH): var.is_parent = True
            else: break

        # check for extensions
        ptr = self.pos-1
        while True:
            ptr += 1
            if ptr >= len(self.tokens): break
            elif self.match_type(ptr, grammar.EXTENSION):
                ext = self.process_extension(self.tokens[ptr])
                var.extensions.append(ext)
            else: break
            
        return var


    def process_extension(self, token):
        match token.value:
            case "upper":
                return extensions.Upper()
            case "lower":
                return extensions.Lower()
            case "quotes":
                return extensions.Quotes()
            case "single-quotes":
                return extensions.SingleQuotes()
            case "escape":
                return extensions.Escape()
            case _:
                raise Exception(f"[Parser] Extension '{token.value}' is invalid")


    def process_foreach(self):
        inner_tokens = []

        while self.current().type != grammar.END:
            inner_tokens.append(self.advance())

        assert inner_tokens[0].type == grammar.VAR, "[Parser] No object assigned to foreach statement"
        self.symbol_table[inner_tokens[0].value] = {"type": "Object", "scope": "Global", "values": {}}
        
        _parser = Parser(inner_tokens[1:], self.symbol_table)
        inner_children, new_symbol_table = _parser.parse()
        self.symbol_table = new_symbol_table

        foreach = nodes.Foreach(inner_tokens[0].value, inner_children)

        return foreach
