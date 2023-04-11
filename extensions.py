import html

class Extension:
	def __init__(self):
		self.name = None
		self.func = None

	def __repr__(self):
		return self.name

	def __call__(self, x):
		return self.func(x)


class Upper(Extension):
	def __init__(self):
		super().__init__()
		self.name = "UpperExtension"
		self.func = lambda x: x.upper()


class Lower(Extension):
	def __init__(self):
		super().__init__()
		self.name = "LowerExtension"
		self.func = lambda x: x.lower()


class Quotes(Extension):
	def __init__(self):
		super().__init__()
		self.name = "QuotesExtension"
		self.func = lambda x: f'"{x}"'


class SingleQuotes(Extension):
	def __init__(self):
		super().__init__()
		self.name = "SingleQuotesExtension"
		self.func = lambda x: f"'{x}'"


class Escape(Extension):
	def __init__(self):
		super().__init__()
		self.name = "EscapeExtension"
		self.func = lambda x: html.escape(x)
