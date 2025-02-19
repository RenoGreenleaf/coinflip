from cmd2 import Cmd
from event.models import Event
from ending.models import Ending
from location.models import Location


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
		if self.current_type == 'events':
			editable = self.pool.get_event(int(args))
		elif self.current_type == 'scenes':
			editable = self.pool.get_scene(int(args))
		else:
			raise Exception("Something went wrong.")

		with self.pool.get_db_session() as session:
			session.delete(editable)
			session.commit()

	def do_exit(self, args):
		print("Leaving.")
		self.state['exit'] = True
		return True

	def do_create(self, args):
		with self.pool.get_db_session() as session:
			if self.current_type == 'events':
				new_event = Event(name="New Event")
				session.add(new_event)
				self.state['current'] = new_event
				return True
			elif self.current_type == 'scenes':
				new_scene = self._scene_by_type(args)
				session.add(new_scene)
				self.state['current'] = new_scene
				return True

	def complete_create(self, text, line, begidx, endidx):
		types = ['ending', 'location']
		return [name for name in types if name.startswith(text)]

	def do_update(self, args):
		"""Make changes to an editable."""
		if self.current_type == 'events':
			editable = self.pool.get_event(int(args))
		elif self.current_type == 'scenes':
			editable = self.pool.get_scene(int(args))
		else:
			raise Exception("Something went wrong.")

		self.state['current'] = editable
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
		for event in self.pool.get_all_events():
			print(f"{event.id} {event}")

	def _list_scenes(self):
		for scene in self.pool.get_all_scenes():
			print(f"{scene.id} {scene}")

	def _scene_by_type(self, typed):
		if typed == 'ending':
			return Ending()
		elif typed == 'location':
			return Location()
		else:
			raise Exception(f"Unknown scene type ({typed}).")
