class Prop:
	def describe(self, events, cli):
		cli.print("This is something.")
		return 'room'

	def use(self, events, cli):
		cli.print("Nothing can be done.")
		return 'room'