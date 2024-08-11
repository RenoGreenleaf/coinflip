#!/usr/bin/env python
from instances.scenes import scenes

current = scenes['menu']

while True:
	next_scene_name = current.play()
	current = scenes[next_scene_name]
