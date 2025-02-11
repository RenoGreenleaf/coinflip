#!/usr/bin/env python
from instances import pool


current_editable = [None]

while True:
	editable = current_editable[0]

	if not editable:
		editable = pool

	editor = editable.wrap_for_editing()
	editor.interact(current_editable)
