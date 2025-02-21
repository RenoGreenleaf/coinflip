from cmd2 import Cmd


class Player(Cmd):
	def __init__(self, location, pool):
		super().__init__()
		self.model = location
		self.pool = pool  # pool is needed because it provides a session

	def interact(self):
		self.cmdloop()
