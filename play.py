#!/usr/bin/env python
from json import load
from instances.pool import Pool


pool = Pool()

with open('pool.json', 'r') as pool_data:
	pool.load(load(pool_data), pool)

sm = pool.get_state_machine()
sm.start_listening()

for scene in pool.get_all_scenes():
	scene.start_listening()

player = sm.get_current_scene().wrap_for_playing(pool)

while True:
	player.interact()
	player = sm.get_current_scene().wrap_for_playing(pool)
