from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser, CompletionItem
from event.models import Event


class Editor(Cmd):
	def item_choices(self):
		"""Item is either an event or a scene."""
		if self.current_type == 'events':
			return [
				CompletionItem(event.id, str(event))
				for event
				in self.pool.get_all_events()
			]
		elif self.current_type == 'scenes':
			return [
				CompletionItem(scene.id, str(scene))
				for scene
				in self.pool.get_all_scenes()
			]
		else:
			raise Exception("Neither scenes nor events are current?")

	def types_choices(self):
		if self.current_type == 'scenes':
			return ['ending', 'location', 'coinflip', 'lock', 'conversation', 'combat']
		else:
			return []

	items_parser = Cmd2ArgumentParser()
	items_parser.add_argument(
		'item_id',
		choices_provider=item_choices,
		type=int
	)

	types_parser = Cmd2ArgumentParser()
	types_parser.add_argument(
		'scene_type',
		choices_provider=types_choices,
		nargs='?'
	)

	def __init__(self, pool):
		super().__init__()
		self.pool = pool
		self.current_type = 'events'
		self.prompt = f"{self.current_type}> "

	def interact(self, state):
		self.state = state
		self.cmdloop()

	def do_list(self, args):
		if self.current_type == 'events':
			self._list_events()
		elif self.current_type == 'scenes':
			self._list_scenes()

	@with_argparser(items_parser)
	def do_delete(self, args):
		if self.current_type == 'events':
			self.pool.delete_event(args.item_id)
		elif self.current_type == 'scenes':
			self.pool.delete_scene(args.item_id)
		else:
			raise Exception("Something went wrong.")

	def do_exit(self, args):
		print("Leaving.")
		self.state['path'].pop()
		return True

	@with_argparser(types_parser)
	def do_create(self, args):
		if self.current_type == 'events':
			event = Event()
			event.id = max(self.pool.events, default=0) + 1
			self.pool.events[event.id] = event
			self.state['path'].append(event)
			return True
		elif self.current_type == 'scenes':
			scene = self._scene_by_type(args.scene_type)
			scene.id = max(self.pool.scenes, default=0) + 1
			self.pool.scenes[scene.id] = scene
			self.state['path'].append(scene)
			return True
		else:
			raise Exception("Mode {self.current_type} is not supported.")

	@with_argparser(items_parser)
	def do_update(self, args):
		"""Make changes to an editable."""
		if self.current_type == 'events':
			editable = self.pool.get_event(args.item_id)
		elif self.current_type == 'scenes':
			editable = self.pool.get_scene(args.item_id)
		else:
			raise Exception("Mode {self.current_type} is not supported.")

		self.state['path'].append(editable)
		return True

	def do_scenes(self, args):
		"""Switches to editing scenes."""
		self._switch('scenes')

	def do_events(self, args):
		"""Switches to editing events."""
		self._switch('events')

	def do_state_machine(self, args):
		self.state['path'].append(self.pool.get_state_machine())
		return True

	def _switch(self, typed):
		"""Select type to work with."""
		self.current_type = typed
		self.prompt = f"{self.current_type}> "

	def _list_events(self):
		for event in self.pool.get_all_events():
			print(f"{event.id} {event}")

	def _list_scenes(self):
		for scene in self.pool.get_all_scenes():
			print(scene)

	def _scene_by_type(self, typed):
		return self.pool.scene_by_type({'type': typed})
