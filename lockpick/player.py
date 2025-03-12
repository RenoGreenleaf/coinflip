from cmd2 import Cmd


class Player(Cmd):
	prompt = "lock> "

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self):
		self.cmdloop()

	def do_clockwise(self, args):
		return self._turn(True)

	def do_counterclockwise(self, args):
		return self._turn(False)

	def _turn(self, is_clockwise):
		if self.model.is_unlocked():
			print("It's already unlocked. Nothing left to do.")
			return True

		direction = 'clockwise' if is_clockwise else 'counterclockwise'
		print(f"You're turning lock-pick {direction}.")

		if self.model.turn(is_clockwise):
			print("\033[92mNice click.\033[0m")
		else:
			print("\033[91mWrong! Back from the start.\033[0m")

		if self.model.is_unlocked():
			print("Yey! It's unlocked.")
			self.model.unlocked_event.trigger()
			return True
