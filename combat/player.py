class Player:
	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self):
		strategies = set(self.model.ai_moves)
		print(f"You can: {", ".join(strategies)}")
		choice = input("Your action: ")

		if choice not in strategies:
			print(f"The action {choice} is unknown.")

		print("Playing a combat.")
