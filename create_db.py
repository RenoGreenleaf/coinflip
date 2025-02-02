from tortoise import Tortoise, run_async


async def foo():
	await Tortoise.init(config_file='./orm-config.json')
	await Tortoise.generate_schemas()

run_async(foo())
