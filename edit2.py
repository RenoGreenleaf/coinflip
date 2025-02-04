from tortoise import Tortoise, run_async
from ending.models import Ending
import settings


run_async(Tortoise.init(settings.TORTOISE))
model = Ending(message="Wrong!")
editor = model.wrap_with_editor()
editor.cmdloop()
