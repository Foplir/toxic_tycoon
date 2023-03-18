from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


from config import TOKEN

START_MESSAGE = "."
CLICK = "оскорбить"
MAGAZINE = "/mag"
BACK = "назад"
UPGRADE_1 = "Первое улучшение - 25$"

bot = Bot(TOKEN)
dp = Dispatcher(bot)
balance=1

def clicking():
	global balance
	balance=balance+1


def get_keyboard(current):
	key = ReplyKeyboardMarkup(resize_keyboard=True)
	if current==0:
		btns = key.add(KeyboardButton(CLICK)).add(KeyboardButton(MAGAZINE))
	elif current==1:
		btns = key.add(KeyboardButton(UPGRADE_1)).add(KeyboardButton(BACK))
	return btns

@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
	await message.reply(text=START_MESSAGE, reply_markup=get_keyboard(0))

@dp.message_handler()
async def answer_on_btn(message: types.Message):
	global balance
	if message.text==MAGAZINE:
		await message.answer(text=".", reply_markup=get_keyboard(1))
		#await message.delete()
	elif message.text==BACK:
		await message.answer(text="back", reply_markup=get_keyboard(0))
		#await message.delete()
	#elif message.text==CLICK:
	#	clicking()
	#	message.answer(text=balance)
		#message.delete()
	else:
		await message.answer(text="0")

if __name__ == "__main__":
	executor.start_polling(dp)
