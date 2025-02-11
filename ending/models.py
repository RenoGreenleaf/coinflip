from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column
from reusables.models import Scene
from ending.editor import Editor


class Ending(Scene):
    __tablename__ = 'ending'
    id = mapped_column(ForeignKey('scene.id'), primary_key=True)
    message = mapped_column(String())

    __mapper_args__ = {
        'polymorphic_identity': 'ending'
    }

    def wrap_with_editor(self):
        return Editor(self)
