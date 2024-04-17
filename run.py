#!/usr/bin/env python
import scenes
from world import World


world = World()
scenes = {
	'coin_flip': scenes.CoinFlip(world),
	'help': scenes.Help(world),
	'exit': scenes.Ending(world)
}
current = scenes['coin_flip']

while True:
	next_scene_name = current.play()
	current = scenes[next_scene_name]
