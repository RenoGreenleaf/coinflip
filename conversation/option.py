from instances.events import events


class Option:
	def __init__(
		self,
		description,
		triggers=events['none'],
		hide_condition=events['none'],
		show_condition=events['none'],
		available=True,
		message=""
	):
		self.description = description
		self.triggers = triggers
		self.hide_condition = hide_condition
		self.show_condition = show_condition
		self.available = available
		self.message = message

	def select(self, cli):
		cli.print(self.message + "\n")
		self.triggers.trigger()

	def is_available(self):
		return self.available

	def describe(self):
		return self.description

	def start_listening(self):
		self.hide_condition.subscribe(self)
		self.show_condition.subscribe(self)

	def notify(self, event):
		if event == self.hide_condition:
			self.available = False
		elif event == self.show_condition:
			self.available = True
