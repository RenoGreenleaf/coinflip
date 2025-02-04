from tortoise.models import Model
from tortoise import fields
from ending.editor import Editor


class Ending(Model):
    id = fields.IntField(primary_key=True)
    message = fields.TextField()

    def wrap_with_editor(self):
        return Editor(self)
