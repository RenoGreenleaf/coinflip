class StateMachine:
	"""Switches scenes."""

	def __init__(
		self,
		transitions,
		scene,
		previous_available,
		previous_requested
	):
		self.transitions = transitions
		self.current_scene = scene
		self.previous_scene = None
		self.previous_available = previous_available
		self.previous_requested = previous_requested

	def start_listening(self):
		for event, _ in self.transitions:
			event.subscribe(self)

		self.previous_requested.subscribe(self)

	def notify(self, triggered_event):
		if triggered_event == self.previous_requested:
			previous = self.current_scene
			self.current_scene = self.previous_scene
			self.previous_scene = previous
			return

		for event, scene in self.transitions:
			if event == triggered_event:
				if self.current_scene != scene:
					self.previous_scene = self.current_scene
					self.previous_available.trigger()

				self.current_scene = scene
				scene.play()
				break

	def get_current_scene(self):
		return self.current_scene
