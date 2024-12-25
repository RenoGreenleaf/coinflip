from scene import scene


class CoinFlip(scene.Scene):
	def __init__(self, cli, events, coin):
		super().__init__(cli, events)
		self.coin = coin
		self.my_score = 0
		self.opponents_score = 0

	def request(self):
		self.cli.print("Choose a side.")

	def execute(self, command):
		if command not in ('heads', 'tails'):
			return super().execute(command)

		fell_on = self.coin.flip()

		if command == fell_on:
			self.i_won.trigger()
			self.my_score += 1
			colour = '\033[92m'
		else:
			self.opponent_won.trigger()
			self.opponents_score += 1
			colour = '\033[91m'

		self.cli.print('The coin fell on ' + colour + fell_on + '\033[0m.')
		self.cli.print(f'{self.my_score}/{self.opponents_score}\n')

	def editable_execute(self, command):
		if command == 'list':
			self._list()
		else:
			self.cli.print("Unclear.")

	def prompt(self):
		return '[heads, tails]> '

	def load(self, scene_data, events):
		self.i_won = events[scene_data['i_won']]
		self.opponent_won = events[scene_data['opponent_won']]

	def serialize(self):
		return {
			'type': 'coin_flip',
			'i_won': self.i_won.serialize(),
			'opponent_won': self.opponent_won.serialize()
		}

	def _list(self):
		self.cli.print("Events:")
		self.cli.print(f"\ti_won: {self.i_won.serialize()}")
		self.cli.print(f"\topponent_won: {self.opponent_won.serialize()}")
