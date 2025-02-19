#!/usr/bin/env python
from instances.pool import Pool


pool = Pool()
state = {'current': pool, 'exit': False}

while True:
	state['current'] = state['current'] or pool
	editor = state['current'].wrap_for_editing(pool)
	editor.interact(state)

	if state['exit']:
		exit()
