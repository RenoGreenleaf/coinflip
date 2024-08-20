from instances import help, menu

from coin_flip.scene import CoinFlip
from lockpick.scene import LockPick
from room.scene import Room
from conversation.scene import Conversation
from ending.scene import Ending

from instances.events import events

from cli import CLI
from coin_flip.coin import Coin
from room.table import Table
from lockpick.lock import Collection


terminal = CLI()
props = {
	'coin': Coin(),
	'locks': Collection(),
	'table': Table(),
}
props['locks'].prepare()
scenes = {
	'coin_flip': CoinFlip(terminal, events, props['coin']),
	'lockpick': LockPick(terminal, events, props['locks']),
	'room': Room(terminal, events, props),
	'menu': Conversation(terminal, events, menu.options, slug='menu'),
	'help': Conversation(terminal, events, help.options, slug='help'),
	'exit': Ending(terminal, events)
}