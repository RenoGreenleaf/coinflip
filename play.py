#!/usr/bin/env python
from main import AI, Player, Event, World

world = World()
turn = Event()
player1 = AI(world)
player2 = Player(world)

turn.subscribe(player1)
turn.subscribe(player2)

world.load({}, None)

while True:
    turn.trigger()
