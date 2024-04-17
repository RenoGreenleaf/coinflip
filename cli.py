class CLI:
	"""Provides explicit access to a command line interface."""
	def input(self, prompt):
		return input(prompt)

	def print(self, text):
		print(text)

	def exit(self):
		exit()