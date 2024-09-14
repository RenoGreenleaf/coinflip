from instances.events import events
from conversation.option import Option


options = []


##################
options.append(Option(
	description="Where am I?",
	message="You're in a playroom.",
	triggers=events['help.asked_where'],
))

##################
options.append(Option(
    description="What can I play here?",
    message="Try coinflip. There's also lock picking game. Lastly, you can turn a table.",
    show_condition=events['help.asked_where'],
    triggers=events['help.asked_what_to_play'],
    available=False
))

##################
options.append(Option(
	description="How to play coinflip?",
	message="""When prompted, specify your preferred side (heads or tails).
Your current score is available in format <your points>/<opponents points>.
It's shown after each flip.""",
	show_condition=events['help.asked_what_to_play'],
	available=False
))

##################
options.append(Option(
    description="How to pick locks?",
    message="""Turn your lockpick left & right.
Correct combination of turns opens a lock.
If a turn is incorrect you have to start over.""",
	show_condition=events['help.asked_what_to_play'],
	available=False
))

##################
options.append(Option(
	description="How to leave?",
	message="""You can leave by typing in "exit"."""
))

##################
options.append(Option(
	description="Back",
	triggers=events['state_machine.previous_requested'],
	show_condition=events['state_machine.previous_scene_available'],
	available=False
))
