from cmd2 import Cmd


class Player(Cmd):
	prompt = "[heads/tails]> "

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self):
		self.cmdloop()

	def do_heads(self, args):
		self.model.flip('heads')
		return self._show_result('heads')

	def do_tails(self, args):
		self.model.flip('tails')
		return self._show_result('tails')

	def _show_result(self, preference):
		if preference == self.model.side:
			colour = '\033[92m'
		else:
			colour = '\033[91m'

		print(f'The coin fell on {colour} {self.model.side}\033[0m.')
		print(f'{self.model.my_score}/{self.model.opponents_score}\n')

		if self.model.is_victory():
			return True
