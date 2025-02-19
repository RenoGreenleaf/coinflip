class Editor:
	def __init__(self, model, pool):
		self.event = model
		self.pool = pool

	def interact(self, state):
		with self.pool.get_db_session() as session:
			session.add(self.event)
			new_name = input(f'Rename "{self.event.name}" to:\n')
			state['current'] = None

			if not new_name:
				return

			self.event.name = new_name
			session.commit()
