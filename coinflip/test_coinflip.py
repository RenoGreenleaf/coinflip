from coinflip import board
from terminal import pieces as term_pieces


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
