class Editor:
	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		new_message = input("New message to be shown when ending:\n")
		state['path'].pop()
		self.model.message = new_message
