import time
import telebot
from telebot import types

from config import TOKEN

bot=telebot.TeleBot(TOKEN)

BALANCE_ = "баланс💲"
CLICK = "оскорбить💢"
MAGAZINE = "купить улучшения✔"
BACK = "назад◀"
UPGRADE_1 = "МАКАКА🐵 - 25$"
UPGRADE_2 = "УРОД😎- 100$"
UPGRADE_3 = "ЧУРКА НЕМЫТАЯ 😡- 500$"
UPGRADE_4 = "БЕС ВСЕЛИЛСЯ🥶- 1000$"
INCREMENT = 1
BALANCE = 0
BUY_SUCCESFUL = "Улучшение успешно куплено!✅"
NOT_ENOUGH_MONEY = "Нехватило средств❌"


def create_btn(name, callback):
	btn = types.InlineKeyboardButton(text=name, callback_data=callback)
	return btn


click = create_btn(CLICK, CLICK)
magazine = create_btn(MAGAZINE, MAGAZINE)
back = create_btn(BACK, BACK)
balance = create_btn(BALANCE_, BALANCE_)
upgrade_1 = create_btn(UPGRADE_1, UPGRADE_1)
upgrade_2 = create_btn(UPGRADE_2, UPGRADE_2)
upgrade_3 = create_btn(UPGRADE_3, UPGRADE_3)
upgrade_4 = create_btn(UPGRADE_4, UPGRADE_4)


state_0 = types.InlineKeyboardMarkup(row_width=4)
state_0.add(click).add(magazine).add(balance)

state_1 = types.InlineKeyboardMarkup(row_width=4)
state_1.add(upgrade_1).add(upgrade_2).add(upgrade_3).add(upgrade_4).add(back)


def buy_upgrade(upgrade):
	global BALANCE
	global INCREMENT
	global BUY_SUCCESFUL

	if upgrade==1 and BALANCE>=25:
		BALANCE=BALANCE-25
		INCREMENT=INCREMENT+1
		return BUY_SUCCESFUL

	if upgrade==2 and BALANCE>=100:
		BALANCE=BALANCE-100
		INCREMENT=INCREMENT+5
		return BUY_SUCCESFUL

	if upgrade==3 and BALANCE>=500:
		BALANCE=BALANCE-500
		INCREMENT=INCREMENT+30
		return BUY_SUCCESFUL

	if upgrade==4 and BALANCE>=1000:
		BALANCE=BALANCE-1000
		INCREMENT=INCREMENT+80
		return BUY_SUCCESFUL

	return NOT_ENOUGH_MONEY

def click():
	global BALANCE
	BALANCE = BALANCE+INCREMENT
	return BALANCE

def edit(txt, state):
	global MAIN_MESSAGE
	global MAIN_ID
	bot.edit_message_text(chat_id=MAIN_MESSAGE, message_id=MAIN_ID.id, text=txt, reply_markup=state)


def delete(message):
	bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['start'])
def start_message(message):
	global MAIN_MESSAGE
	global MAIN_ID
	MAIN_MESSAGE = message.chat.id
	bot.send_message(message.chat.id, "Hi!")
	MAIN_ID = bot.send_message(message.chat.id, "Toxic Tycoon", reply_markup=state_0)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	global BALANCE

	if call.data == MAGAZINE:
		edit(MAGAZINE, state_1)
		bot.send_message(call.message.chat.id, '')

	elif call.data == BACK:
		edit("Toxic Tycoon", state_0)
		bot.send_message(call.message.chat.id, '')

	elif call.data == BALANCE_:
		current_balance = "Ваш текущий баланс: "+str(BALANCE)+"$"
		edit(current_balance, state_0)
		bot.send_message(call.message.chat.id, '')
		time.sleep(2)
		edit("Toxic Tycoon", state_0)
	elif call.data == CLICK:
		click()
		bot.send_message(call.message.chat.id, '')

@bot.message_handler()
def button_handler(message):
	if message.text==UPGRADE_1:
		bot.send_message(message.chat.id, buy_upgrade(1))
		bot.delete_message(message.chat.id, message.message_id)
	elif message.text==UPGRADE_2:
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, buy_upgrade(2))
	elif message.text==UPGRADE_3:
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, buy_upgrade(3))
	elif message.text==UPGRADE_4:
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, buy_upgrade(4))
bot.infinity_polling()

