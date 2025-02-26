#!/usr/bin/env python
from instances.pool import Pool


pool = Pool()

with pool.get_db_session() as session:
	sm = pool.get_state_machine()
	event = sm.transitions[0].event

	session.add(sm)
	sm.start_listening()

	# for scene in pool.get_all_scenes():
	# 	scene.start_listening()

	event.trigger()
	player = sm.get_current_scene().wrap_for_playing(pool)
	player.interact()
