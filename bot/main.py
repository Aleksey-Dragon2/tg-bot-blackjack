import telebot
from handlers import *
import settings
from common import bot

# bot = telebot.TeleBot(settings.TOKEN)

bot.message_handler(commands=['start'])(start)
bot.message_handler()(game_process)

bot.infinity_polling()