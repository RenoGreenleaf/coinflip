from scenes import scene


class LockPick(scene.Scene):
	def __init__(self, cli, events, lock):
		super().__init__(cli, events)
		self.slug = 'lockpick'
		self.lock = lock

	def request(self):
		self.cli.print("Turn the lock-pick.")

	def execute(self, command):
		if command == 'left':
			success = self.lock.turn(False)
		elif command == 'right':
			success = self.lock.turn(True)
		else:
			return super().execute(command)

		if success:
			self.cli.print("Nice click.\n")
		else:
			self.cli.print("Wrong! Back from the start.\n")

		if self.lock.unlocked():
			self.cli.print("Yey! It's unlocked.\n")
			return 'menu'

		return self.slug

	def prompt(self):
		return '[left, right]> '