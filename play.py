#!/usr/bin/env python
import json

from main import World, EmptyRelationships


def load(persistent):
    with open('world.json', 'r') as world_file:
        world_data = json.load(world_file)
        persistent.load(world_data, EmptyRelationships())


def mainloop(world):
    while True:
        option = world.get_option()
        message = option.get_message()
        world.process(message)


world = World()
load(world)
mainloop(world)
