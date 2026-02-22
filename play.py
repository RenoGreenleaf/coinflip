#!/usr/bin/env python
# Copyright (C) 2026  Reno Greenleaf
"""Entry point."""
from json import load
from coinflip.pieces import Event
from coinflip.board import World
from terminal.players import System
from AI.players import AI


relationships: dict = {}

with open('coinflip.json', 'r', encoding='utf-8') as world_file:
    json = load(world_file)

    world = World(**json['board'])
    world.persist(relationships)
    turn = Event(identifier=1000)
    player1 = AI(world)
    player2 = System(world)

    turn.subscribe(player1)
    turn.subscribe(player2)

    player1.load(json, relationships)
    player2.load(json, relationships)

del relationships

while True:
    turn.trigger()
