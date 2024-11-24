class Prop:
	def __init__(self, triggers):
		self.triggers = triggers

	def describe(self, events, cli):
		cli.print("This is something.")

	def use(self, events, cli):
		cli.print("Nothing can be done.")
		self.triggers.trigger()
