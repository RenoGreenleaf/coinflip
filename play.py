#!/usr/bin/env python
from json import load
from main import AI, Player, Event, World

world = World()
turn = Event()
player1 = AI(world)
player2 = Player(world)

turn.subscribe(player1)
turn.subscribe(player2)

with open('coinflip.json', 'r') as world_file:
    world.load(load(world_file), None)

world.unid('option')

while True:
    turn.trigger()
