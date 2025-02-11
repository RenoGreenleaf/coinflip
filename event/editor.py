from reusables.session import Session


class Editor:
	def __init__(self, model):
		self.event = model

	def interact(self, current_editable):
		new_name = input(f'Rename {self.event.name} to:\n')

		if not new_name:
			current_editable[0] = None
			return

		self.event.name = new_name

		with Session() as session:
			session.add(self.event)
			session.commit()

		current_editable[0] = None
