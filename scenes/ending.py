from scenes import scene


class Ending(scene.Scene):
	def play(self):
		self.cli.print("Bye-bye!")
		self.cli.exit()