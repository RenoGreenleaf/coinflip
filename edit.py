#!/usr/bin/env python
from instances.pool import Pool
from json import load, dump


pool = Pool()

with open('pool.json', 'r') as pool_data:
	pool.load(load(pool_data), pool)

state = {'path': [pool]}

while state['path'] != []:
	editor = state['path'][-1].wrap_for_editing(pool)
	editor.interact(state)

	print("Saving.")

	with open('pool.json', 'w') as pool_data:
		dump(pool.save(), pool_data, sort_keys=True, indent=4)
