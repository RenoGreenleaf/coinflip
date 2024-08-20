from event.event import Event, Irrelevant


events = {
	'none': Irrelevant(),
	'coinflip.i_won': Event(),
	'coinflip.opponent_won': Event(),
	'scene.decided_to_exit': Event(),
	'scene.asked_for_help': Event(),
	'scene.asked_for_menu': Event(),
	'help.asked_where': Event(),
	'help.games_known': Event(),
	'help.asked_what_to_play': Event()
}