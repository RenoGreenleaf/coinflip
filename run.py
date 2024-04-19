#!/usr/bin/env python
import help, menu
from scenes import coin_flip, conversation, ending, lockpick, room
from cli import CLI
from coin import Coin
from lock import Collection


terminal = CLI()
events = set()
props = {
	'coin': Coin(),
	'locks': Collection()
}
props['locks'].prepare()
scenes = {
	'coin_flip': coin_flip.CoinFlip(terminal, events, props['coin']),
	'lockpick': lockpick.LockPick(terminal, events, props['locks']),
	'room': room.Room(terminal, events, props),
	'menu': conversation.Conversation(terminal, events, menu.options, slug='menu'),
	'help': conversation.Conversation(terminal, events, help.options, slug='help'),
	'exit': ending.Ending(terminal, events)
}
current = scenes['menu']

while True:
	next_scene_name = current.play()
	current = scenes[next_scene_name]
