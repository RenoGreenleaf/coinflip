#!/usr/bin/env python
from instances.scenes import scenes
from instances.events import events
from editor.editor import Editor
from cli import CLI


editor = Editor(CLI(), events, scenes)

while True:
	editor.edit()
