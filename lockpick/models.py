from sqlalchemy import Integer, Boolean, ForeignKey, inspect, select
from sqlalchemy.orm import mapped_column, relationship, reconstructor
from reusables.models import Scene, Model
from event.models import Event
from lockpick.editor import Editor
from lockpick.player import Player


class Lock(Scene):
	__tablename__ = 'lock'
	__mapper_args__ = {
		'polymorphic_identity': 'lock',
		'polymorphic_load': 'selectin'
	}
	id = mapped_column(ForeignKey(Scene.id), primary_key=True)
	unlocked_event_id = mapped_column(
		ForeignKey(Event.id),
		nullable=False,
		default=0
	)
	unlocked_event = relationship(
		Event,
		lazy='joined',
		foreign_keys=unlocked_event_id
	)
	pins = relationship(
		'Pin',
		back_populates='lock',
		lazy='selectin',
		cascade='all, delete-orphan'
	)

	@reconstructor
	def prepare(self):
		self.position = 0

	def turn(self, is_clockwise):
		if self.pins[self.position].is_clockwise == is_clockwise:
			self.position += 1
			return True
		else:
			self.position = 0
			return False

	def is_unlocked(self):
		return self.position == len(self.pins)

	def add_pin(self, is_clockwise):
		session = inspect(self).session
		last_pin = session.scalars(
			select(Pin).where(Pin.lock == self).order_by(Pin.offset.desc())
		).first()
		offset = 0 if last_pin is None else last_pin.offset + 1
		pin = Pin(offset=offset, is_clockwise=is_clockwise)
		self.pins.append(pin)

	def delete_pin(self, offset):
		for pin in self.pins:
			if pin.offset == offset:
				break

		self.pins.remove(pin)

		for offset, pin in zip(range(len(self.pins)), self.pins):
			pin.offset = offset

	def switch_pin(self, offset):
		for pin in self.pins:
			if pin.offset == offset:
				break

		pin.is_clockwise = not pin.is_clockwise
		return pin.is_clockwise

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def wrap_for_playing(self, pool):
		return Player(self, pool)

	def set_unlocked(self, event_id):
		self.unlocked_event_id = event_id

	def __repr__(self):
		amount = len(self.pins)
		return f"Lock with {amount} pins"


class Pin(Model):
	__tablename__ = 'lock_pin'
	id = mapped_column(Integer(), primary_key=True)
	is_clockwise = mapped_column(Boolean(), nullable=False)
	lock_id = mapped_column(ForeignKey(Lock.id), nullable=False)
	offset = mapped_column(Integer(), nullable=False)  # for sorting
	lock = relationship(
		Lock,
		lazy='joined',
		back_populates='pins',
		foreign_keys=lock_id
	)

	def __repr__(self):
		direction = 'clockwise' if self.is_clockwise else 'counterclockwise'
		return f"Pin #{self.offset}, {direction}"
