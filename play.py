#!/usr/bin/env python
from state_machine.state_machine import StateMachine
from instances import scenes, state_machine, events
from player.player import Player


state_machine = StateMachine(
	state_machine.transitions,
	state_machine.current_scene,
	state_machine.previous_scene_available,
	state_machine.previous_requested,
)
state_machine.start_listening()

for scene in scenes.scenes.values():
	scene.start_listening()

player = Player(events.events)
player.cmdloop()
