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

	def editable_execute(self, command):
		if command == 'list':
			self._list()
		else:
			self.cli.print("Unclear.")

	def _list(self):
		self.cli.print(f"Message: {self.message}")
