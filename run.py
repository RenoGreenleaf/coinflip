#!/usr/bin/env python
import help
from scenes import coin_flip, conversation, ending
from cli import CLI
from coin import Coin


terminal = CLI()
events = set()
props = {
	'coin': Coin()
}
scenes = {
	'coin_flip': coin_flip.CoinFlip(terminal, events, props),
	'help': conversation.Conversation(terminal, events, help.options),
	'exit': ending.Ending(terminal, events)
}
current = scenes['coin_flip']

while True:
	next_scene_name = current.play()
	current = scenes[next_scene_name]
