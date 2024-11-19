from json import load

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
scenes = {}

with open('instances/scenes.json', 'r') as scenes_file:
	scenes_data = load(scenes_file)

	for scene_name, scene_data in scenes_data.items():
		if scene_data['type'] == 'exit':
			scene = Ending(terminal, events)
		elif scene_data['type'] == 'coin_flip':
			scene = CoinFlip(terminal, events, props['coin'])
		elif scene_data['type'] == 'lockpick':
			scene = LockPick(terminal, events, props['locks'])
		elif scene_data['type'] == 'room':
			scene = Room(terminal, events, props)
		elif scene_data['type'] == 'conversation':
			scene = Conversation(terminal, events, [])
		else:
			raise Exception("Unknown scene type.")

		scene.load(scene_data, events)
		scenes[scene_name] = scene
