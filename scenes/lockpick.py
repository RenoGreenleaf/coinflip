from scenes import scene


class LockPick(scene.Scene):
	def __init__(self, cli, events):
		super().__init__(cli, events)
		self.slug = 'lockpick'

	def request(self):
		super().request()

	def execute(self, command):
		return super().execute(command)

	def prompt(self):
		return '[left, right]> '