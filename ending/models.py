from reusables.models import Scene
from ending.editor import Editor
from ending.player import Player


class Ending(Scene):
	def __init__(self):
		self.id = 0
		self.message = ""

	def save(self):
		return {
			'id': self.id,
			'type': 'ending',
			'message': self.message
		}

	def load(self, dictionary, pool):
		self.id = dictionary['id']
		self.message = dictionary['message']

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def __repr__(self):
		return f"Ending ({self.message[:15]})"
