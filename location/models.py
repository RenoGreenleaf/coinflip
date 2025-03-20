from reusables.models import Scene
from location.editor import Editor
from location.player import Player


class Location(Scene):
	"""Things to explore."""
	def __init__(self):
		self.description = ""
		self.exits = []
		self.discovered_event = None

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
		self.triggers_event = None

	def __repr__(self):
		return f"Exit ({self.name})"
