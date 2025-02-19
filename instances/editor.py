from cmd2 import Cmd
from reusables.session import Session
from event.models import Event
from ending.models import Ending
from room.models import Room


class Editor(Cmd):
	def __init__(self, pool):
		super().__init__()
		self.pool = pool
		self.current_type = 'events'
		self.prompt = f"{self.current_type}> "

	def update_pool(self, pool):
		self.pool = pool

	def interact(self, state):
		self.state = state
		self.cmdloop()

	def do_list(self, args):
		if self.current_type == 'events':
			self._list_events()
		elif self.current_type == 'scenes':
			self._list_scenes()

	def do_delete(self, args):
		editable = self.pool[self.current_type].pop(int(args))

		with Session() as session:
			session.delete(editable)
			session.commit()

	def do_exit(self, args):
		print("Leaving.")
		self.state['exit'] = True
		return True

	def do_create(self, args):
		if self.current_type == 'events':
			new_event = Event(name="New Event")
			self.state['current'] = new_event
			return True
		elif self.current_type == 'scenes':
			new_scene = self._scene_by_type(args)
			self.state['current'] = new_scene
			return True

	def complete_create(self, text, line, begidx, endidx):
		types = ['ending', 'room']
		return [name for name in types if name.startswith(text)]

	def do_update(self, args):
		"""Make changes to an editable."""
		self.state['current'] = self.pool[self.current_type][int(args)]
		return True

	def do_scenes(self, args):
		"""Switches to editing scenes."""
		self._switch('scenes')

	def do_events(self, args):
		"""Switches to editing events."""
		self._switch('events')

	def _switch(self, typed):
		"""Select type to work with."""
		self.current_type = typed
		self.prompt = f"{self.current_type}> "

	def _list_events(self):
		for identifier, event in self.pool['events'].items():
			print(f"{identifier} {event}")

	def _list_scenes(self):
		for identifier, scene in self.pool['scenes'].items():
			print(f"{identifier} {scene}")

	def _scene_by_type(self, typed):
		if typed == 'ending':
			return Ending()
		elif typed == 'room':
			return Room()
		else:
			raise Exception(f"Unknown scene type ({typed}).")
