from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column
from reusables.models import Scene
from ending.editor import Editor


class Ending(Scene):
	__tablename__ = 'ending'
	__mapper_args__ = {
		'polymorphic_identity': 'ending',
		'polymorphic_load': 'selectin'
	}
	id = mapped_column(ForeignKey('scene.id'), primary_key=True)
	message = mapped_column(String())

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def __repr__(self):
		return f"Ending ({self.message[:15]})"
