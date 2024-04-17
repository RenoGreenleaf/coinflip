from option import Option


options = []


def where(events, cli):
	cli.print("You're in a simple coin flipping game.\n")
	events.add('help.where')

options.append(Option(
	"Where am I?",
	where
))


def location_known(events):
	return 'help.where' in events

def how(events, cli):
	cli.print("When prompted, specify your preferred side (heads or tails).")
	cli.print("Your current score is available in format <your points>/<opponents points>.")
	cli.print("It's shown after each flip.\n")

options.append(Option(
	"How to play it?",
	how,
	location_known
))


def leave(events, cli):
	cli.print('You can leave by typing in "exit".\n')

options.append(Option(
	"How to leave?",
	leave
))
