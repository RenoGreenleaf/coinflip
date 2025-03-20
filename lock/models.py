from reusables.models import Scene
from event.models import Event
from lock.editor import Editor
from lock.player import Player


class Lock(Scene):
	def __init__(self):
		self.position = 0

		self.unlocked_event = None
		self.pins = []

	def turn(self, is_clockwise):
		if self.pins[self.position].is_clockwise == is_clockwise:
			self.position += 1
			return True
		else:
			self.position = 0
			return False

	def is_unlocked(self):
		return self.position == len(self.pins)

	def add_pin(self, is_clockwise):
		pin = Pin()
		pin.is_clockwise = is_clockwise
		self.pins.append(pin)

	def delete_pin(self, offset):
		del self.pins[offset]

	def switch_pin(self, offset):
		pin = self.pins[offset]
		pin.is_clockwise = not pin.is_clockwise
		return pin.is_clockwise

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def __repr__(self):
		amount = len(self.pins)
		return f"Lock with {amount} pins"


class Pin:
	def __init__(self):
		self.is_clockwise = True

	def __repr__(self):
		direction = 'clockwise' if self.is_clockwise else 'counterclockwise'
		return f"{direction} pin"
