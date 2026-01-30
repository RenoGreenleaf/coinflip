#!/usr/bin/env python
# Copyright (C) 2026  Reno Greenleaf
"""Entry point."""
from json import load
import board
import players

world = board.World()
turn = board.Event()
player1 = players.AI(world)
player2 = players.System(world)

turn.subscribe(player1)
turn.subscribe(player2)

with open('coinflip.json', 'r', encoding='utf-8') as world_file:
    json = load(world_file)
    world.load(json, world)
    player1.load(json, world)
    player2.load(json, world)

world.unid('option')

while True:
    turn.trigger()
