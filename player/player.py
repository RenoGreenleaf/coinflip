from cmd import Cmd


class Player(Cmd):
	"""Handles interaction with a user via CLI."""

	def __init__(self, events):
		super().__init__()
		self.exit = events['ui.exit']

	def do_exit(self, args):
		self.exit.trigger()
