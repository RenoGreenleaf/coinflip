from sqlalchemy import ForeignKey, String, Boolean, Integer
from sqlalchemy.orm import mapped_column, relationship, reconstructor
from reusables.models import Model, Scene
from event.models import Event
from conversation.editor import Editor, OptionEditor
from conversation.player import Player


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

	def wrap_for_playing(self, pool):
		return Player(self, pool)

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

	def get_options(self):
		return [option for option in self.options if option.is_available]

	def start_listening(self):
		for option in self.options:
			option.start_listening()

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
	# whether an option is available *by default*
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

	@reconstructor
	def prepare(self):
		self.is_available = self.available

	def wrap_for_editing(self, pool):
		return OptionEditor(self, pool)

	def start_listening(self):
		self.hide.subscribe(self)
		self.show.subscribe(self)

	def notify(self, event):
		if event == self.show:
			self.is_available = True
		elif event == self.hide:
			self.is_available = False
		else:
			raise Exception(
				"An option is notified about event that's not subscribed to."
			)

	def __repr__(self):
		return f"Option ({self.description[:10]}…)"
