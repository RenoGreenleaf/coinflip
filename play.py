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
    json = load(world_file)
    world.load(json, world)
    player1.load(json, world)
    player2.load(json, world)

world.unid('option')

while True:
    turn.trigger()
