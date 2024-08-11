from scene.prop import Prop


class Table(Prop):
	def __init__(self):
		self.side = True

	def describe(self, events, cli):
		if self.side:
			cli.print("A large wooden table stands in the centre of the room.\n")
		else:
			cli.print("A small decorated glass table stands here.\n")
		return 'room'

	def use(self, events, cli):
		self.side = not self.side
		cli.print("Turning the table changed its properties.\n")
		return 'room'
