from option import Option


options = []


def select_coin_flip(events, cli):
	cli.print("Playing coin flip.")
	return 'coin_flip'

options.append(Option(
	"Coin flip",
	select_coin_flip
))


def select_lockpick(events, cli):
	return 'lockpick'

options.append(Option(
	"Lock-pick",
	select_lockpick
))


def select_exploration(events, cli):
	return 'room'

options.append(Option(
	"Explore",
	select_exploration
))


def select_help(events, cli):
	return 'help'

options.append(Option(
	"Help",
	select_help
))