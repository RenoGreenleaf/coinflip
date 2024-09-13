from instances.events import events
from instances.scenes import scenes


transitions = [
	(events['scene.asked_for_menu'], scenes['menu']),
	(events['scene.decided_to_exit'], scenes['exit']),
	(events['scene.asked_for_help'], scenes['help']),
	(events['menu.coinflip_selected'], scenes['coin_flip']),
	(events['menu.lockpick_selected'], scenes['lockpick']),
	(events['menu.exploration_selected'], scenes['room']),
	(events['menu.help_selected'], scenes['help']),
]
current_scene = scenes['menu']
previous_scene_available = events['state_machine.previous_scene_available']
previous_requested = events['state_machine.previous_requested']
