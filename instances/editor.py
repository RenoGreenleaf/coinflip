from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser, CompletionItem
from event.models import Event
from ending.models import Ending
from location.models import Location
from coin_flip.models import CoinFlip
from lockpick.models import Lock


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
			return ['ending', 'location', 'coin_flip']
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
			editable = self.pool.get_event(args.item_id)
		elif self.current_type == 'scenes':
			editable = self.pool.get_scene(args.item_id)
		else:
			raise Exception("Something went wrong.")

		with self.pool.get_db_session() as session:
			session.delete(editable)
			session.commit()

	def do_exit(self, args):
		print("Leaving.")
		self.state['path'].pop()
		return True

	@with_argparser(types_parser)
	def do_create(self, args):
		with self.pool.get_db_session() as session:
			if self.current_type == 'events':
				new_event = Event(name="New Event")
				session.add(new_event)
				self.state['path'].append(new_event)
				return True
			elif self.current_type == 'scenes':
				new_scene = self._scene_by_type(args.scene_type)
				session.add(new_scene)
				self.state['path'].append(new_scene)
				return True

	@with_argparser(items_parser)
	def do_update(self, args):
		"""Make changes to an editable."""
		if self.current_type == 'events':
			editable = self.pool.get_event(args.item_id)
		elif self.current_type == 'scenes':
			editable = self.pool.get_scene(args.item_id)
		else:
			raise Exception("Something went wrong.")

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
			print(f"{scene.id} {scene}")

	def _scene_by_type(self, typed):
		if typed == 'ending':
			return Ending()
		elif typed == 'location':
			return Location()
		elif typed == 'coin_flip':
			return CoinFlip()
		else:
			raise Exception(f"Unknown scene type ({typed}).")
