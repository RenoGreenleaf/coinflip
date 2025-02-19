class Editor():
	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		new_message = input("New message to be shown when ending:\n")
		state['current'] = None

		if not new_message:
			return

		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.message = new_message
			session.commit()
