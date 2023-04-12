class Compiler:
	def __init__(self, syntax_tree, data):
		self.out = ""
		self.syntax_tree = syntax_tree
		self.data = data


	def compile(self):
		for node in self.syntax_tree:
			self.process_node(node)

		return self.out


	def process_node(self, node):
		match repr(node):
			case "HTMLBlock":
				self.out += node.value
			case "Variable":
				self.out += self.apply_extensions(self.data[node.name], node.extensions)
			case "ForeachStatement":
				self.process_foreach(node)


	def process_foreach(self, node):
		# iterate over each element in list
		for obj in self.data[node.parent]:
			# iterate over each token in block
			for i, child in enumerate(node.children):
				if repr(child) == "HTMLBlock":
					self.out += child.value
				else:
					self.out += self.apply_extensions(obj[child.name], child.extensions)


	def apply_extensions(self, value, extensions):
		for ex in extensions:
			value = ex(value)

		return value
