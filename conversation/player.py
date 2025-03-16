class Player:
	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self):
		self.list_options()
		choice = input("> ")
		options = self.model.get_options()
		option = options[int(choice) - 1]
		print(option.message or option.description)
		option.triggers.trigger()

	def list_options(self):
		index = 0

		for option in self.model.get_options():
			index += 1
			print(f"{index}. {option.description}")
