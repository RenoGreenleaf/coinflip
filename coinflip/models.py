from random import choice
from reusables.models import Scene
from event.models import Event
from coinflip.editor import Editor
from coinflip.player import Player


class CoinFlip(Scene):
	def __init__(self):
		self.victory_threshold = 3
		self.won_event = None

		self.my_score = 0
		self.opponents_score = 0

	def flip(self, preference):
		self.side = choice(['tails', 'heads'])

		if preference == self.side:
			self.my_score += 1
		else:
			self.opponents_score += 1

		if self.is_victory():
			self.won_event.trigger()

	def is_victory(self):
		return self.my_score - self.opponents_score >= self.victory_threshold

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def set_threshold(self, threshold):
		self.victory_threshold = threshold

	def __repr__(self):
		return f"CoinFlip (triggers {self.won_event} after {self.victory_threshold} wins)"