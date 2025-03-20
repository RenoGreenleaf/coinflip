from event.models import Event
from state_machine.models import StateMachine
from instances.editor import Editor

from ending.models import Ending
from location.models import Location
from coinflip.models import CoinFlip
from lock.models import Lock
from conversation.models import Conversation


class Pool:

	def __init__(self):
		self.editor = None
		self.scenes = {}
		self.events = {}
		self.state_machine = None

	def load(self, dictionary):
		for identifier, event_data in dictionary['events'].items():
			event = Event()
			event.load(event_data, self)
			self.events[identifier] = event

		for identifier, scene_data in dictionary['scenes'].items():
			scene = self.scene_by_type(scene_data)
			scene.load(scene_data, self)
			self.scenes[identifier] = scene

		self.state_machine = StateMachine()
		self.state_machine.load(dictionary['state_machine'])

	def save(self):
		result = {'events': {}, 'scenes': {}, 'state_machine': {}}

		for identifier, event in self.events.items():
			result['events'][identifier] = event.save()

		for identifier, scene in self.scenes.items():
			result['scenes'][identifier] = scene.save()

		result['state_machine'] = self.state_machine.save()
		return result

	def scene_by_type(self, dictionary):
		typed = dictionary['type']

		if typed == 'ending':
			scene = Ending()
		elif typed == 'location':
			scene = Location()
		elif typed == 'coin_flip':
			scene = CoinFlip()
		elif typed == 'lock':
			scene = Lock()
		elif typed == 'conversation':
			scene = Conversation()
		else:
			raise Exception(f"Unknown scene type ({typed}).")

		return scene

	def get_all_events(self):
		return self.events.values()

	def get_all_scenes(self):
		return self.scenes.values()

	def get_event(self, identifier):
		return self.events[identifier]

	def get_scene(self, identifier):
		return self.scenes[identifier]

	def get_state_machine(self):
		if not self.state_machine:
			self.state_machine = StateMachine()

		return self.state_machine

	def delete_event(self, identifier):
		del self.events[identifier]

	def delete_scene(self, identifier):
		del self.scenes[identifier]

	def wrap_for_editing(self, pool):
		if not self.editor:
			self.editor = Editor(pool)

		return self.editor
