from reusables.models import Scene
from reusables import nulls
from lock.editor import Editor
from lock.player import Player


class Lock(Scene):
	def __init__(self):
		self.id = 0
		self.unlocked_event = nulls.event
		self.pins = []

		self.position = 0

	def save(self):
		result = {
			'id': self.id,
			'type': 'lock',
			'unlocked_event': self.unlocked_event.id,
			'pins': []
		}

		for pin in self.pins:
			result['pins'].append({
				'is_clockwise': pin.is_clockwise
			})

		return result

	def load(self, dictionary, pool):
		self.id = dictionary['id']
		self.unlocked_event = pool.get_event(dictionary['unlocked_event'])

		for pin_data in dictionary['pins']:
			pin = Pin()
			pin.is_clockwise = pin_data['is_clockwise']
			self.pins.append(pin)

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

	def delete_pin(self, index):
		del self.pins[index]

	def switch_pin(self, index):
		pin = self.pins[index]
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
