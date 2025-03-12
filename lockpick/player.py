from cmd2 import Cmd


class Player(Cmd):
	prompt = "lock> "

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self):
		self.cmdloop()
