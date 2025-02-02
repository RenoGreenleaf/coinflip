from tortoise.models import Model
from tortoise import fields


class Ending(Model):
    id = fields.IntField(primary_key=True)
    message = fields.TextField()
