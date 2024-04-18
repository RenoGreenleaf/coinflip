from scenes import scene


class CoinFlip(scene.Scene):
	def __init__(self, cli, events, props):
		super().__init__(cli, events)
		self.slug = 'coin_flip'
		self.coin = props['coin']
		self.my_score = 0
		self.opponents_score = 0

	def request(self):
		self.cli.print("Choose a side (heads, tails).")

	def execute(self, command):
		if command not in ('heads', 'tails'):
			return super().execute(command)

		fell_on = self.coin.flip()

		if command == fell_on:
			self.my_score += 1
			colour = '\033[92m'
		else:
			self.opponents_score += 1
			colour = '\033[91m'

		self.cli.print('The coin fell on ' + colour + fell_on + '\033[0m.')
		self.cli.print(f'{self.my_score}/{self.opponents_score}\n')
		return self.slug