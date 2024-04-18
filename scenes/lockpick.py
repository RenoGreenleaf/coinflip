from scenes import scene


class LockPick(scene.Scene):
	def __init__(self, cli, events, locks):
		super().__init__(cli, events)
		self.slug = 'lockpick'
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
			self.cli.print("Nice click.\n")
		else:
			self.cli.print("Wrong! Back from the start.\n")

		if lock.unlocked():
			self.cli.print("Yey! It's unlocked.\n")
			return 'menu'

		return self.slug

	def prompt(self):
		return '[left, right]> '