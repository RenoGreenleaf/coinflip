#!/usr/bin/env python
from instances.pool import Pool


pool = Pool()
current_editable = [None]

while True:
	editable = current_editable[0]

	if not editable:
		editable = pool
		editable.update()

	editor = editable.wrap_for_editing()
	editor.interact(current_editable)

	if editable == pool and not current_editable[0]:
		exit()
