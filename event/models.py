from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from reusables.model import Model


class Event(Model):
	__tablename__ = 'event'

	id = mapped_column(Integer(), primary_key=True)
	name = mapped_column(String(255), nullable=False)
