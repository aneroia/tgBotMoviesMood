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

last_command = ""

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


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    words = message.text.split()  # Разбиваем сообщение пользователя на слова
    if len(words) > 0:
        random_word = random.choice(words)  # Выбираем случайное слово
        bot.send_message(message.chat.id, random_word)



bot.polling()