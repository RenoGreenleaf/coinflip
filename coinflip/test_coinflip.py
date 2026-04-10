# Copyright (C) 2026  Reno Greenleaf
import copy
from coinflip import board, pieces
from terminal import pieces as term_pieces


class Subscriber:
	def __init__(self):
		self.processed = False

	def process(self, event):
		self.processed = True


def test_world_persistence():
	relationships = {}
	conversation = term_pieces.Conversation(identifier=1)
	world = board.World(identifier=2, conversations=[conversation])
	expected = {
		'1': conversation,
		'2': world,
	}

	world.persist(relationships)

	assert relationships == expected


def test_ai_node():
	node = pieces.Piece()
	untouched = copy.copy(node)

	node.act(0)

	assert node == untouched


def test_event():
	subscriber = Subscriber()
	event = pieces.Piece()
	event.subscribe(subscriber)

	event.trigger()

	assert subscriber.processed


def test_children():
	node = pieces.Piece()

	assert node.children == []


def test_description():
	node = pieces.Piece()
	untouched = copy.copy(node)

	node.describe("A text.")

	assert node == untouched


def test_hash():
	event = pieces.Piece()
	dictionary = {event: None}

	assert event in dictionary


def test_stringable():
	node = pieces.Piece()

	text = str(node)

	assert text == '<no title>'
