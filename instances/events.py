from event.event import Event


events = {
	'coinflip.i_won': Event(),
	'coinflip.opponent_won': Event(),
	'scene.decided_to_exit': Event(),
	'scene.asked_for_help': Event(),
	'scene.asked_for_menu': Event()
}