#!/usr/bin/env python
from instances.pool import Pool


pool = Pool()
state = {'path': [pool]}

while state['path'] != []:
	editor = state['path'][-1].wrap_for_editing(pool)
	editor.interact(state)
