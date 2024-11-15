from instances.events import events
from instances.scenes import scenes
from json import load

transitions = []

with open('instances/state_machine.json', 'r') as sm_json:
	sm_data = load(sm_json)

	for event_name, scene_name in sm_data['transitions'].items():
		transitions.append((events[event_name], scenes[scene_name]))

	current_scene = scenes[sm_data['current_scene']]
	previous_scene_available = events[sm_data['previous_scene_available']]
	previous_requested = events[sm_data['previous_requested']]
