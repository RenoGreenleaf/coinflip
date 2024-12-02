from scene import scene


class Ending(scene.Scene):
	def play(self):
		self.cli.print(self.message)
		self.cli.exit()

	def load(self, scene_data, events):
		self.message = scene_data.get('message', "")

	def serialize(self):
		return {
			'type': 'exit',
			'message': self.message
		}

	def get_structure(self):
		return {
			('message', "Message shown on exit."): self.message
		}
