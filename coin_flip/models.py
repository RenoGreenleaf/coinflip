from random import choice
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, reconstructor
from reusables.models import Scene
from event.models import Event
from coin_flip.editor import Editor


class CoinFlip(Scene):
	__tablename__ = 'coin_flip'
	__mapper_args__ = {
		'polymorphic_identity': 'coin_flip',
		'polymorphic_load': 'selectin'
	}
	id = mapped_column(ForeignKey(Scene.id), primary_key=True)
	won_event_id = mapped_column(ForeignKey(Event.id))
	won_event = relationship(
		Event,
		foreign_keys=(won_event_id,),
		lazy='joined'
	)

	@reconstructor
	def prepare(self):
		self.my_score = 0
		self.opponents_score = 0

	def flip(self, preference):
		side = choice(['tails', 'heads'])

		if preference == side:
			self.won_event.trigger()
			self.my_score += 1
			colour = '\033[92m'
		else:
			self.opponents_score += 1
			colour = '\033[91m'

		self.cli.print(f'The coin fell on {colour} {side}\033[0m.')
		self.cli.print(f'{self.my_score}/{self.opponents_score}\n')

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def set_won_event(self, event_id):
		self.won_event_id = event_id

	def __repr__(self):
		return f"CoinFlip (triggers {self.won_event})"