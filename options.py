from option import Option


options = []


def where(events):
	print("You're in a simple coin flipping game.\n")
	events.add('help.where')

options.append(Option(
	"Where am I?",
	where
))


def location_known(events):
	return 'help.where' in events

def how(events):
	print("When prompted, specify your preferred side (heads or tails).")
	print("Your current score is available in format <your points>/<opponents points>.")
	print("It's shown after each flip.\n")

options.append(Option(
	"How to play it?",
	how,
	location_known
))


def leave(events):
	print('You can leave by typing in "exit".\n')

options.append(Option(
	"How to leave?",
	leave
))
