import pickle
import time
import telebot
from telebot import types

from config import TOKEN

bot=telebot.TeleBot(TOKEN)

BALANCE_ = "баланс💲"
CLICK = "оскорбить💢"
MAGAZINE = "купить улучшения✔"
BACK = "назад◀"

UPGRADES = ["МАКАКА🐵 - 25$", "УРОД😎- 100$", "ЧУРКА НЕМЫТАЯ 😡- 500$", "БЕС ВСЕЛИЛСЯ🥶- 1000$", "ПОН🤐- 5000$", "ЛОШАРА🤣- 10000$", "БАБУБЭ😱- 100000$"]
COSTS = [25, 100, 500, 1000, 5000, 10000, 100000]
INCREMENTS = [1, 5, 30, 80, 500, 1200, 15000]

INCREMENT = 1
BALANCE = 0

BUY_SUCCESFUL = "Улучшение успешно куплено!✅"
NOT_ENOUGH_MONEY = "Нехватило средств❌"

PLAYER = {}

def create_btn(name):
	btn = types.InlineKeyboardButton(text=name, callback_data=name)
	return btn


#buttons
click = create_btn(CLICK)
magazine = create_btn(MAGAZINE)
back = create_btn(BACK)
balance = create_btn(BALANCE_)

state_0 = types.InlineKeyboardMarkup(row_width=4)
state_0.add(click).add(magazine).add(balance)

state_1 = types.InlineKeyboardMarkup(row_width=4)
for i in range(len(UPGRADES)):
	state_1.add(create_btn(UPGRADES[i]))
state_1.add(back)



def buy_upgrade(upgrade, message):
	global BALANCE, INCREMENT

	if BALANCE>=COSTS[upgrade]:
		BALANCE=BALANCE-COSTS[upgrade]
		INCREMENT=INCREMENT+INCREMENTS[upgrade]
		msg = bot.send_message(message.chat.id, BUY_SUCCESFUL)
		time.sleep(2)
		bot.delete_message(message.chat.id, msg.message_id)

	else:
		msg = bot.send_message(message.chat.id, NOT_ENOUGH_MONEY)
		time.sleep(2)
		bot.delete_message(message.chat.id, msg.message_id)

def click():
	global BALANCE, PLAYER
	BALANCE = BALANCE+INCREMENT


	with open(str(USER_ID), "w") as f:
		f.writelines(str(BALANCE)+"\n")
		f.writelines(str(INCREMENT))

	return BALANCE

def edit(txt, state):
	global MAIN_MESSAGE
	global MAIN_ID
	bot.edit_message_text(chat_id=MAIN_MESSAGE, message_id=MAIN_ID.id, text=txt, reply_markup=state)


def delete(message):
	bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['start'])
def start_message(message):
	global BALANCE, INCREMENT, MAIN_MESSAGE, MAIN_ID, USER_ID
	MAIN_MESSAGE = message.chat.id
	bot.send_message(message.chat.id, "Hi!")
	MAIN_ID = bot.send_message(message.chat.id, "Toxic Tycoon", reply_markup=state_0)
	USER_ID = message.from_user.id


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	global BALANCE

	if call.data == MAGAZINE:
		edit(MAGAZINE, state_1)

	elif call.data == BACK:
		edit("Toxic Tycoon", state_0)

	elif call.data == BALANCE_:
		current_balance = "Ваш текущий баланс: "+str(BALANCE)+"$"
		msg = bot.send_message(call.message.chat.id, current_balance)
		time.sleep(1)
		bot.delete_message(call.message.chat.id, msg.message_id)

	elif call.data == CLICK:
		click()

	for i in range(len(UPGRADES)):
		if call.data == UPGRADES[i]:
			buy_upgrade(i, call.message)


bot.infinity_polling()

