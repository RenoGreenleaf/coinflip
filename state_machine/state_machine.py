class StateMachine:
	"""Switches scenes."""

	def __init__(self, scenes, events):
		self.transitions = [
			(events['scene.asked_for_menu'], scenes['menu']),
			(events['scene.decided_to_exit'], scenes['exit']),
			(events['scene.asked_for_help'], scenes['help'])
		]
		self.current_scene = scenes['coin_flip']

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