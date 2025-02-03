from tortoise.models import Model
from tortoise import fields


class Event(Model):
	id = fields.IntField(primary_key=True)
	name = fields.CharField(max_length=255)
