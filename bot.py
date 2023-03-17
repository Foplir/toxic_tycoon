from aiogram import Bot, executor, Dispatcher, types

from config import TOKEN


bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
	await message.reply(text="ХАХАХХА")
