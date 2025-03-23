from reusables.nulls import Editor, Player


class Scene:
	def start_listening(self):
		pass

	def notify(self):
		pass

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

