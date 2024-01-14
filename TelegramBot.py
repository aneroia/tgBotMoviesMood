import telebot
import random
from telebot import types

bot = telebot.TeleBot("6776361176:AAEQNFDg6KQsM4ALYu5grGQgpuPTt0dAByE")

hello_message = '''👋 Hello! I'm MovieMoodBot!\n 
🤖 I'm your personal movie assistant. Just tell me about your mood 
or how your day went, and I'll help you find the perfect movie for today.\n
🔥 Ready to dive into the world of cinema? Just message me, and let's get started!\n
📌 Write /help for more information.'''


help_message = '''📌 Here's a little instruction on how to work with me:\n
✉️ Write me about how your day went (up to 100 characters).\n
📈 I will analyze your mood and suggest you a selection of movies that fit your mood.\n
🎬 Press "start" to begin!'''

writeMe_message = 'Write me about your day (up to 100 characters):'

last_message = ""
message_flag = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("🎬 Let's get started")
    markup.add(btn)
    bot.reply_to(message, hello_message, reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/start")
    markup.add(btn1)
    bot.reply_to(message, help_message, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "🎬 Let's get started")
def handle_start(message):
    bot.send_message(message.chat.id, writeMe_message)
    bot.register_next_step_handler(message, get_random_word)

@bot.message_handler(func=lambda message: message.text == "↩️ Back to start")
def handle_backtostart(message):
    bot.register_next_step_handler(message, send_welcome)


def get_random_word(message):
    global message_flag
    global last_message
    if not message_flag:
        last_message = message.text
        message_flag = True
        words = message.text.split()  # Разбиваем сообщение пользователя на слова
        if len(words) > 0:
            random_word = random.choice(words)  # Выбираем случайное слово
            bot.send_message(message.chat.id, random_word)
            show_options_keyboard(message)
    elif message_flag:
        words = last_message.split()  # Разбиваем сообщение пользователя на слова
        if len(words) > 0:
            random_word = random.choice(words)  # Выбираем случайное слово
            bot.send_message(message.chat.id, random_word)
            show_options_keyboard(message)


def show_options_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📼 More")
    btn2 = types.KeyboardButton("✉️ New Message")
    btn3 = types.KeyboardButton("↩️ Back to start")
    btn4 = types.KeyboardButton("⭐️ Rate this selection")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "🛠 Choose the option:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_options)

def handle_options(message):
    global message_flag
    if message.text == '📼 More':
        bot.send_message(message.chat.id, "📼 New selection of movies:")
        get_random_word(message)
    elif message.text == '✉️ New Message':
        message_flag = False
        bot.send_message(message.chat.id, writeMe_message)
        bot.register_next_step_handler(message, get_random_word)
    elif message.text == '↩️ Back to start':
        message_flag = False
        send_welcome(message)
    elif message.text == '⭐️ Rate this selection':
        message_flag = False
        rate_buttons(message)

@bot.message_handler(func=lambda message: message.text == "⭐️ Rate this selection")
def rate_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("1")
    btn2 = types.KeyboardButton("2")
    btn3 = types.KeyboardButton("3")
    btn4 = types.KeyboardButton("4")
    btn5 = types.KeyboardButton("5")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, "Оцените по шкале от 1 до 5", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.isdigit() and int(message.text) in range(1, 6))
def handle_rating(message):
    bot.send_message(message.chat.id, "Спасибо за обратную связь")
    markup = types.ReplyKeyboardMarkup(row_width=1)
    start_button = types.KeyboardButton("↩️ Back to start")
    markup.add(start_button)
    bot.send_message(message.chat.id, "Вы можете вернуться в начало", reply_markup=markup)


bot.polling()