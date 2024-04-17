from options import options
from coin import Coin


class Scene:
	"""Commonly available commands."""
	def __init__(self, world):
		self.slug = ''
		self.cli = world['cli']

	def request(self):
		"""Asks what to do next."""
		print("Enter a command")

	def execute(self, command):
		if command == 'help':
			return 'help'
		elif command == 'exit':
			return 'exit'
		else:
			print("Unclear.\n")
			return self.slug

	def prompt(self):
		"""Prefixes users input."""
		return '> '

	def play(self):
		self.request()
		command = self.cli.input(self.prompt())
		return self.execute(command)


class CoinFlip(Scene):
	def __init__(self, world):
		super().__init__(world)
		self.slug = 'coin_flip'
		self.coin = Coin()
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


class Help(Scene):
	def __init__(self, world):
		super().__init__(world)
		self.slug = 'help'
		self.events = world['events']
		self.available_options = []

	def request(self):
		item = 0
		self.available_options = []

		for option in options:
			self._add_option(option)

		for option in self.available_options:
			item += 1
			self.cli.print(f'{item}. {option.describe()}')

		self.cli.print(f'{item+1}. Back.')

	def execute(self, command):
		if not command.isnumeric():
			return super().execute(command)

		if int(command) == len(self.available_options) + 1:  # "back" option is chosen.
			return 'coin_flip'

		option = self.available_options[int(command) - 1]
		option.select(self.events, self.cli)
		return self.slug

	def prompt(self):
		return f'[1-{len(self.available_options)+1}]> '

	def _add_option(self, option):
		if option.is_available(self.events):
			self.available_options.append(option)