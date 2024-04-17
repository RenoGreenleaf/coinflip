#!/usr/bin/env python
import scenes
from world import World


world = World()
scenes = {
	'coin_flip': scenes.CoinFlip(world),
	'help': scenes.Help(world)
}
current = scenes['coin_flip']

while True:
	next_scene_name = current.play()

	if next_scene_name == 'exit':
		world['cli'].print("Bye-bye!")
		break

	current = scenes[next_scene_name]