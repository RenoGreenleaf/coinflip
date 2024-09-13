from conversation.option import Option
from instances.events import events


options = []

##################
options.append(Option(
	description="Coin flip",
	message="Playing coin flip.",
	triggers=events['menu.coinflip_selected']
))

##################
options.append(Option(
	description="Lock-pick",
	triggers=events['menu.lockpick_selected']
))

##################
options.append(Option(
	description="Explore",
	triggers=events['menu.exploration_selected']
))

##################
options.append(Option(
	description="Help",
	triggers=events['menu.help_selected']
))

##################
options.append(Option(
	description="Back",
	triggers=events['state_machine.previous_requested'],
	show_condition=events['state_machine.previous_scene_available'],
	available=False
))
