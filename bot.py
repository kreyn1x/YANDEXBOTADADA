import telebot
from info import help_message, First_lvl_text, Locations, Locations_butt1,Locations_view, finals, finals2, Locations_butt2, Locations_photo1, Locations_photo2
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
TOKEN = "6628153752:AAFmsh_tAJgUrmn981JbM1q-bdaL37nlPoE"
bot = telebot.TeleBot(TOKEN)
global user_data
user_data = {}

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton('/start'))
markup.add(KeyboardButton('/start_quest'))
markup.add(KeyboardButton('/help'))



@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, text="Пропишите /star_quest для начала квеста, или /help чтобы увидеть все команды", reply_markup = markup)
    global chat_id
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {}
        if "lvl" not in user_data[chat_id]:
            user_data[chat_id]["lvl"] = 0
            print(user_data)
        if "loc" not in user_data[chat_id]:
            user_data[chat_id]["loc"] = 0
            print(user_data)
        if "winORlose" not in user_data[chat_id]:
            user_data[chat_id]["winORlose"] = 0

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, text=help_message, reply_markup = markup)

@bot.message_handler(commands=['start_quest'], content_types=['text'])
def handle_start_quest(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Да")
    button2 = KeyboardButton("Начать заново")
    button3 = KeyboardButton("/start")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Вы готовы начать ?", reply_markup=markup)
    bot.register_next_step_handler(message, check_user_progress)


def First_lvl(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Таможня")
    button2 = KeyboardButton("Лес")
    button3 = KeyboardButton("Завод")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, First_lvl_text, reply_markup=markup)
    bot.register_next_step_handler(message, check)


def Quest(message):
    chat_id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(Locations_butt1[user_data[chat_id]["lvl"]][user_data[chat_id]["loc"]]))
    markup.add(KeyboardButton(Locations_butt2[user_data[chat_id]["lvl"]][user_data[chat_id]["loc"]]))
    bot.send_message(message.chat.id, Locations_view[user_data[chat_id]["lvl"]][user_data[chat_id]["loc"]], reply_markup=markup)
    bot.send_photo(message.from_user.id, photo=open(Locations_photo1[user_data[chat_id]["lvl"]][user_data[chat_id]["loc"]], 'rb'), reply_markup=markup)
    bot.send_photo(message.from_user.id, photo=open(Locations_photo2[user_data[chat_id]["lvl"]][user_data[chat_id]["loc"]], 'rb'), reply_markup=markup)
    print(user_data)
    bot.register_next_step_handler(message, mainHome)

def Final(message):
    chat_id
    if user_data[chat_id]["lvl"] == 3:
        bot.send_message(message.chat.id, finals2[user_data[chat_id]["winORlose"]], reply_markup=markup)

    elif user_data[chat_id]["winORlose"] > 0:
        chat_id
        bot.send_message(message.chat.id, finals[user_data[chat_id]["lvl"]][user_data[chat_id]["winORlose"]], reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Пройдите квест чтобы получить результат",reply_markup=markup)

def check(message):
    if message.text == "Таможня":
        user_data[chat_id]["lvl"] += 2
        user_data[chat_id]["loc"] += 0
        Quest(message)
    if message.text == "Лес":
        user_data[chat_id]["lvl"] += 1
        user_data[chat_id]["loc"] += 0
        Quest(message)
    if message.text == "Завод":
        user_data[chat_id]["lvl"] += 3
        user_data[chat_id]["loc"] += 0
        Quest(message)
    if message.text not in Locations:
        bot.send_message(message.chat.id, "Введите один из вариантов ответа", reply_markup=markup)
        First_lvl(message)

def check_user_progress(message):
    if message.text == "Да":
        if user_data[chat_id]["lvl"] == 0:
            First_lvl(message)

        elif user_data[chat_id]["winORlose"] > 0:
            bot.send_message(message.chat.id, "Вы уже прошли тест, вывожу результат", reply_markup=markup)
            Final(message)

        else:
            Quest(message)

    elif message.text == "Начать заново":
        user_data[chat_id]["lvl"] = 0
        user_data[chat_id]["loc"] = 0
        user_data[chat_id]["winORlose"] = 0
        First_lvl(message)


def mainHome(message):
    chat_id
    if user_data[chat_id]["lvl"] == 1:
        if message.text == "Подвалы":
            user_data[chat_id]["winORlose"] += 1
            Final(message)
        elif message.text == "Автомастерская":
            user_data[chat_id]["winORlose"] += 2
            Final(message)
        elif message.text == "32гб":
            user_data[chat_id]["winORlose"] += 3
            Final(message)
        elif message.text == "16гб":
            user_data[chat_id]["winORlose"] += 4
            Final(message)

        elif message.text == "Пропушу":
            user_data[chat_id]["loc"] += 1
            Quest(message)
        elif message.text == "В кустах":
            user_data[chat_id]["loc"] += 2
            Quest(message)
        else:
            bot.send_message(message.chat.id, "Введите один из вариантов ответа", reply_markup=markup)
            Quest(message)

    if user_data[chat_id]["lvl"] == 2:
        if message.text == "В кустах":
            user_data[chat_id]["winORlose"] += 1
            Final(message)
        elif message.text == "Пропущу":
            user_data[chat_id]["winORlose"] += 2
            Final(message)
        elif message.text == "Деревню":
            user_data[chat_id]["winORlose"] += 3
            Final(message)
        elif message.text == "Санаторий":
            user_data[chat_id]["winORlose"] += 4
            Final(message)

        elif message.text == "АГС":
            user_data[chat_id]["loc"] += 1
            Quest(message)
        elif message.text == "Общага":
            user_data[chat_id]["loc"] += 2
            Quest(message)
        else:
            bot.send_message(message.chat.id, "Введите один из вариантов ответа", reply_markup=markup)
            Quest(message)

    if user_data[chat_id]["lvl"] == 3:
        if message.text == "Пропушу":
            user_data[chat_id]["winORlose"] += 1
            Final(message)

        elif message.text == "Тихонько пойду":
            user_data[chat_id]["winORlose"] += +2
            Final(message)
        else:
            bot.send_message(message.chat.id, "Введите один из вариантов ответа", reply_markup=markup)
            Quest(message)




bot.polling()