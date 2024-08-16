#!/usr/bin/env python
from state_machine.state_machine import StateMachine
from instances import events, scenes

state_machine = StateMachine(scenes.scenes, events.events)
state_machine.start_listening()

while True:
	scene = state_machine.get_current_scene()
	scene.play()
