#!/usr/bin/env python
from scenes import coin_flip, help, ending
from cli import CLI


terminal = CLI()
events = set()
scenes = {
	'coin_flip': coin_flip.CoinFlip(terminal, events),
	'help': help.Help(terminal, events),
	'exit': ending.Ending(terminal, events)
}
current = scenes['coin_flip']

while True:
	next_scene_name = current.play()
	current = scenes[next_scene_name]
