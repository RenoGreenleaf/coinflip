from cmd import Cmd
from reusables.session import Session
from event.models import Event


class Editor(Cmd):
	def __init__(self, events):
		super().__init__()
		self.events = events

	def interact(self, current_editable):
		self.current_editable = current_editable
		self.cmdloop()

	def do_list(self, args):
		for identifier, event in self.events.items():
			print(f"{identifier} {event}")

	def do_delete(self, args):
		event = self.events.pop(int(args))

		with Session() as session:
			session.delete(event)
			session.commit()

	def do_exit(self, args):
		print("Leaving.")
		exit()

	# TODO: following functions require state machine

	def do_create(self, args):
		new_event = Event(name="New Event")
		self.current_editable[0] = new_event
		return True

	def do_update(self, args):
		self.current_editable[0] = self.events[int(args)]
		return True
