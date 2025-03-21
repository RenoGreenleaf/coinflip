from reusables.models import Scene
from reusables import nulls
from location.editor import Editor
from location.player import Player


class Location(Scene):
	"""Things to explore."""
	def __init__(self):
		self.id = 0
		self.description = ""
		self.exits = []
		self.discovered_event = nulls.event

	def save(self):
		result = {
			'id': self.id,
			'type': 'location',
			'description': self.description,
			'discovered_event': self.discovered_event.id,
			'exits': []
		}

		for exit_ in self.exits:
			result['exits'].append({
				'name': exit_.name,
				'description': exit_.description,
				'triggers_event': exit_.triggers_event.id
			})

		return result

	def load(self, dictionary, pool):
		self.exits = []
		self.id = dictionary['id']
		self.description = dictionary['description']
		self.discovered_event = pool.get_event(dictionary['discovered_event'])

		for exit_data in dictionary['exits']:
			exit_ = Exit()
			exit_.name = exit_data['name']
			exit_.description = exit_data['description']
			exit_.triggers_event = pool.get_event(exit_data['triggers_event'])
			self.exits.append(exit_)

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def find_exits(self, startswith):
		return [exit_ for exit_ in self.exits if exit_.name.startswith(startswith)]

	def find_exit_by_name(self, name):
		exits = [exit_ for exit_ in self.exits if exit_.name == name]

		if exits:
			return exits[0]
		else:
			raise Exception(f"There's no exit named {name}")

	def find_exit_by_id(self, identifier):
		for exit_ in self.exits:
			if exit_.id == identifier:
				return exit_

	def add_exit(self, name, triggers_event=None):
		exit_ = Exit()
		exit_.name = name
		exit_.triggers_event = triggers_event
		self.exits.append(exit_)

	def delete_exit(self, identifier):
		for exit_ in self.exits:
			if exit_.id == identifier:
				to_delete = exit_
				break

		self.exits.remove(to_delete)

	def __repr__(self):
		return f"Location ({self.description[:15]}…)"


class Exit:
	def __init__(self):
		self.name = ""
		self.description = ""
		self.triggers_event = nulls.event

	def __repr__(self):
		return f"Exit ({self.name})"
