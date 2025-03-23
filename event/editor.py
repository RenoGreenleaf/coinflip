class Editor:
	def __init__(self, model, pool):
		self.model = model
		self.pool = pool

	def interact(self, state):
		new_name = input("New event name: ")
		state['path'].pop()

		if not new_name:
			return

		self.model.name = new_name
