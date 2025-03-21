from reusables import nulls
from state_machine.editor import Editor


class StateMachine:
	def __init__(self):
		self.transitions = []
		self.start = nulls.scene

		self.current_scene = self.start

	def save(self):
		result = {
			'start': self.start.id,
			'transitions': []
		}

		for transition in self.transitions:
			result['transitions'].append({
				'scene': transition.scene.id,
				'event': transition.event.id
			})

		return result

	def load(self, dictionary, pool):
		self.start = pool.get_scene(dictionary['start'])

		for transition_data in dictionary['transitions']:
			transition = Transition()
			transition.scene = pool.get_scene(transition_data['scene'])
			transition.event = pool.get_event(transition_data['event'])
			self.transitions.append(transition)

	def start_listening(self):
		for transition in self.transitions:
			transition.event.subscribe(self)

	def notify(self, triggered_event):
		for transition in self.transitions:
			if transition.event == triggered_event:
				self.current_scene = transition.scene
				break

	def get_current_scene(self):
		return self.current_scene

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def add_transition(self, scene, event):
		transition = Transition()
		transition.scene = scene
		transition.event = event
		self.transitions.append(transition)

	def delete_transition(self, index):
		del self.transitions[index]

	def set_start(self, scene):
		self.start = scene

	def __repr__(self):
		count = len(self.transitions)
		return f"State machine with {count} transitions."


class Transition:
	def __init__(self):
		self.event = nulls.event
		self.scene = nulls.scene

	def __repr__(self):
		return f"To {self.scene} by {self.event}"
