from option import Option


options = []


def where():
	print("You're in a simple coin flipping game.\n")

options.append(Option(
	"Where am I?",
	where
))


def how():
	print("When prompted, specify your preferred side (heads or tails).")
	print("Your current score is available in format <your points>/<opponents points>.")
	print("It's shown after each flip.\n")

options.append(Option(
	"How to play it?",
	how
))


def leave():
	print('You can leave by typing in "exit".\n')

options.append(Option(
	"How to leave?",
	leave
))
