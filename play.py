#!/usr/bin/env python
from instances.pool import Pool


pool = Pool()

with pool.get_db_session() as session:
	sm = pool.get_state_machine()
	session.add(sm)
	sm.start_listening()

	# for scene in pool.get_all_scenes():
	# 	scene.start_listening()

	player = sm.get_current_scene().wrap_for_playing(pool)

	while True:
		player.interact()
		player = sm.get_current_scene().wrap_for_playing(pool)
