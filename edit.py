#!/usr/bin/env python
# Copyright (C) 2026  Reno Greenleaf
import cmd2
from instances.pool import Pool
from json import load, dump


del cmd2.Cmd.do_edit
del cmd2.Cmd.do_eof
del cmd2.Cmd.do_history
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

state = {'path': [pool]}

while state['path'] != []:
	editor = state['path'][-1].wrap_for_editing(pool)
	editor.interact(state)

	print("Saving.")

	with open('pool.json', 'w') as pool_data:
		dump(pool.save(), pool_data, indent=4)
