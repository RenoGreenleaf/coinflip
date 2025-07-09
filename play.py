#!/usr/bin/env python
from main import World


world = World()

while True:
	option = world.get_option()
	message = option.get_message()
	world.process(message)
