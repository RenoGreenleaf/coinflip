#!/usr/bin/env python
# Copyright (C) 2026  Reno Greenleaf
"""Entry point."""
from json import load
import board
import players


relationships: dict = {}
world = board.World()
turn = board.Event()
player1 = players.AI(world)
player2 = players.System(world)

turn.subscribe(player1)
turn.subscribe(player2)

with open('coinflip.json', 'r', encoding='utf-8') as world_file:
    json = load(world_file)
    world.load(json, relationships)
    player1.load(json, relationships)
    player2.load(json, relationships)

del relationships

while True:
    turn.trigger()
