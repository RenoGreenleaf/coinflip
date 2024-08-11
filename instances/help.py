from conversation.option import Option


options = []


##################
def where(events, cli):
	cli.print("You're in a playroom.\n")
	events.add('help.where')

options.append(Option(
	"Where am I?",
	where
))


##################
def games_to_play(events, cli):
    cli.print("Try coinflip. There's also lock picking game. Lastly, you can turn a table.\n")
    events.add('help.games_known')

def location_known(events):
	return 'help.where' in events

options.append(Option(
    "What can I play here?",
    games_to_play,
    location_known
))


##################
def how_coinflip(events, cli):
	cli.print("When prompted, specify your preferred side (heads or tails).")
	cli.print("Your current score is available in format <your points>/<opponents points>.")
	cli.print("It's shown after each flip.\n")

def games_known(events):
    return 'help.games_known' in events

options.append(Option(
	"How to play coinflip?",
	how_coinflip,
	games_known
))


##################
def how_lockpick(events, cli):
    cli.print("Turn your lockpick left & right.")
    cli.print("Correct combination of turns opens a lock.")
    cli.print("If a turn is incorrect you have to start over.\n")

options.append(Option(
    "How to pick locks?",
    how_lockpick,
    games_known
))


##################
def leave(events, cli):
	cli.print('You can leave by typing in "exit".\n')

options.append(Option(
	"How to leave?",
	leave
))
