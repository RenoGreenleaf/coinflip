class StateMachine:
	"""Switches scenes."""

	def __init__(self, transitions, scene):
		self.transitions = transitions
		self.current_scene = scene

	def start_listening(self):
		for event, _ in self.transitions:
			event.subscribe(self)

	def notify(self, triggered_event):
		for event, scene in self.transitions:
			if event == triggered_event:
				self.current_scene = scene
				break

	def get_current_scene(self):
		return self.current_scene