from scenes import scene


class Room(scene.Scene):
	"""A location to explore."""
	def __init__(self, cli, events, props):
		super().__init__(cli, events)
		self.props = props
		self.slug = 'room'

	def request(self):
		self.cli.print("The room is large.")
		self.cli.print("There's a pile of locks in a corner")
		self.cli.print("and a coin is lying on the floor.")
		self.cli.print("There's also a table.")

	def execute(self, command):
		words = command.split()

		if len(words) != 2:
			return super().execute(command)
		else:
			action, item_name = words

		if item_name not in self.props:
			self.cli.print(f"There's no {item_name} here.\n")
			return self.slug

		if action == 'describe':
			return self.props[item_name].describe(self.events, self.cli)
		elif action == 'use':
			return self.props[item_name].use(self.events, self.cli)
		else:
			self.cli.print(f"That can't be done with the {item_name}.\n")

		return self.slug
