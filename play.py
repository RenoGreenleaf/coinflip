#!/usr/bin/env python
import cmd2
from json import load
from instances.pool import Pool


del cmd2.Cmd.do_alias
del cmd2.Cmd.do_edit
del cmd2.Cmd.do_eof
del cmd2.Cmd.do_ipy
del cmd2.Cmd.do_py
del cmd2.Cmd.do_quit
del cmd2.Cmd.do_set
del cmd2.Cmd.do_shell
del cmd2.Cmd.do_shortcuts
del cmd2.Cmd.do_run_pyscript
del cmd2.Cmd.do_run_script

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
