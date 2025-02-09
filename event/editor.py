class Editor:
	def __init__(self, model):
		self.event = model

	def interact(self):
		new_name = input(f'Rename {self.event.name} to:\n')
		self.event.name = new_name
