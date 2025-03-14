"""UIs for null objects."""


class Editor:
	def __init__(self, model, pool):
		self.model = model

	def interact(self, state):
		print(f"\033[91m{self.model} can't be edited.\033[0m")
		state['path'].pop()


class Player:
	def __init__(self, model, pool):
		self.model = model

	def interact(self):
		raise Exception(f"\033[91mError (stumbled into {self.model})!.\033[0m")
