from options import options
from coin import Coin


class Scene:
	"""Commonly available commands."""
	def __init__(self):
		self.slug = ''

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
		command = input(self.prompt())
		return self.execute(command)


class CoinFlip(Scene):
	def __init__(self):
		self.slug = 'coin_flip'
		self.coin = Coin()
		self.my_score = 0
		self.opponents_score = 0

	def request(self):
		print("Choose a side (heads, tails).")

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

		print('The coin fell on ' + colour + fell_on + '\033[0m.')
		print(f'{self.my_score}/{self.opponents_score}\n')
		return self.slug


class Help(Scene):
	def __init__(self):
		self.slug = 'help'

	def request(self):
		item = 0

		for option in options:
			item += 1
			print(f'{item}. {option.describe()}')

		print(f'{item+1}. Back.')

	def execute(self, command):
		if not command.isnumeric():
			return super().execute(command)

		if int(command) == len(options) + 1:  # "back" option is chosen.
			return 'coin_flip'

		option = options[int(command) - 1]
		option.select()
		return self.slug

	def prompt(self):
		return f'[1-{len(options)+1}]> '
