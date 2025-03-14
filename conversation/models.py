from sqlalchemy import ForeignKey, String, Boolean, Integer
from sqlalchemy.orm import mapped_column, relationship, reconstructor
from reusables.models import Model, Scene
from event.models import Event
from conversation.editor import Editor, OptionEditor


class Conversation(Scene):
	__tablename__ = 'conversation'
	__mapper_args__ = {
		'polymorphic_identity': 'conversation',
		'polymorphic_load': 'selectin'
	}
	id = mapped_column(ForeignKey(Scene.id), primary_key=True)
	options = relationship(
		'Option',
		back_populates='conversation',
		lazy='selectin',
		cascade='all, delete-orphan'
	)

	@reconstructor
	def prepare(self):
		self.available_options = []

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def add_option(self):
		option = Option()
		self.options.append(option)
		return option

	def get_option(self, identifier):
		for option in self.options:
			if option.id == identifier:
				return option

	def delete_option(self, identifier):
		for option in self.options:
			if option.id == identifier:
				self.options.remove(option)

	def __repr__(self):
		return f"Conversation #{self.id} with {len(self.options)} Options"


class Option(Model):
	__tablename__ = 'conversation_option'
	id = mapped_column(Integer(), primary_key=True)
	conversation_id = mapped_column(
		ForeignKey(Conversation.id),
		nullable=False,
		default=0
	)
	description = mapped_column(String(), nullable=False, default="")
	triggers_id = mapped_column(ForeignKey(Event.id), nullable=False, default=0)
	hide_id = mapped_column(ForeignKey(Event.id), nullable=False, default=0)
	show_id = mapped_column(ForeignKey(Event.id), nullable=False, default=0)
	available = mapped_column(Boolean, nullable=False, default=True)
	message = mapped_column(String(), nullable=False, default="")
	conversation = relationship(
		Conversation,
		lazy='joined',
		back_populates='options',
		foreign_keys=conversation_id
	)
	triggers = relationship(Event, lazy='joined', foreign_keys=triggers_id)
	hide = relationship(Event, lazy='joined', foreign_keys=hide_id)
	show = relationship(Event, lazy='joined', foreign_keys=show_id)

	def wrap_for_editing(self, pool):
		return OptionEditor(self, pool)

	def __repr__(self):
		return f"Option ({self.description[:10]}…)"
