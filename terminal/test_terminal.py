from terminal import pieces


def test_option_description():
	option = pieces.Option()
	description = "An option."

	option.describe(description)

	assert str(option) == description


def test_conversation_persistence():
	relationships = {}
	option = pieces.Option(identifier=2)
	conversation = pieces.Conversation(identifier=1, options=[option])
	expected = {
		'1': conversation,
		'2': option,
	}

	conversation.persist(relationships)

	assert relationships == expected


def test_conversation_description():
	conversation = pieces.Conversation()
	description = "A conversation."

	conversation.describe(description)

	assert str(conversation) == description
