class Player:
	def __init__(self, model, pool):
		self.model = model
		self.pool = pool

	def interact(self):
		print(self.model.message)
		exit()
