from scene import scene


class LockPick(scene.Scene):
	def __init__(self, cli, events, locks):
		super().__init__(cli, events)
		self.locks = locks

	def request(self):
		self.cli.print("Turn the lock-pick.")

	def execute(self, command):
		lock = self.locks.pull()

		if command == 'left':
			success = lock.turn(False)
		elif command == 'right':
			success = lock.turn(True)
		else:
			return super().execute(command)

		if success:
			self.cli.print("\033[92mNice click.\033[0m\n")
		else:
			self.cli.print("\033[91mWrong! Back from the start.\033[0m\n")

		if lock.unlocked():
			self.cli.print("Yey! It's unlocked.\n")

	def prompt(self):
		return '[left, right]> '

	def serialize(self):
		return {
			'type': 'lockpick'
		}
