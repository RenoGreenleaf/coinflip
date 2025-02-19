from reusables.session import Session


class Editor:
	def __init__(self, model):
		self.event = model

	def interact(self, state):
		new_name = input(f'Rename "{self.event.name}" to:\n')
		state['current'] = None

		if not new_name:
			return

		self.event.name = new_name

		with Session() as session:
			session.add(self.event)
			session.commit()
