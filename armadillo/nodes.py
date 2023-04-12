class Variable:
    def __init__(self, name, required=False, extensions=None, parent=None):
        self.name = name
        self.required = required
        self.extensions = extensions or []
        self.parent = parent

    def __repr__(self):
        return "Variable"

    def apply_extensions(self):
        for ex in self.extensions:
            self.value = ex(self.value)

    def get_name(self):
        if self.parent:
            return f'{self.parent}.{self.name}'
        else:
            return self.name


class Foreach:
    def __init__(self, parent, children):
        self.parent = parent
        self.children = children

    def __repr__(self):
        return "ForeachStatement"


class HTML:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "HTMLBlock"
