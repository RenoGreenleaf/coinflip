#!/usr/bin/env python
import scenes
from cli import CLI


terminal = CLI()
events = set()
scenes = {
	'coin_flip': scenes.CoinFlip(terminal, events),
	'help': scenes.Help(terminal, events),
	'exit': scenes.Ending(terminal, events)
}
current = scenes['coin_flip']

while True:
	next_scene_name = current.play()
	current = scenes[next_scene_name]
