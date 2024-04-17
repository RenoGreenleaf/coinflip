#!/usr/bin/env python
import scenes


scenes = {
	'coin_flip': scenes.CoinFlip(),
	'help': scenes.Help()
}
current = scenes['coin_flip']

while True:
	next_scene_name = current.play()

	if next_scene_name == 'exit':
		print("Bye-bye!")
		break

	current = scenes[next_scene_name]