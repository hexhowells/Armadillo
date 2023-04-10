import html

upper = lambda x: x.upper()
lower = lambda x: x.lower()
quotes = lambda x: f'"{x}"'
single_quotes = lambda x: f"'{x}'"
escape = lambda x: html.escape(x)
