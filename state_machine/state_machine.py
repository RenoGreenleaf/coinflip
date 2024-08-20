class StateMachine:
	"""Switches scenes."""

	def __init__(self, scenes, events):
		self.transitions = [# TODO: move that to instances.
			(events['scene.asked_for_menu'], scenes['menu']),
			(events['scene.decided_to_exit'], scenes['exit']),
			(events['scene.asked_for_help'], scenes['help']),
			(events['menu.coinflip_selected'], scenes['coin_flip']),
			(events['menu.lockpick_selected'], scenes['lockpick']),
			(events['menu.exploration_selected'], scenes['room']),
			(events['menu.help_selected'], scenes['help']),
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