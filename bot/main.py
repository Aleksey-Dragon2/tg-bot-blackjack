import telebot
from bot.handlers import *
import config.settings
from bot.common import bot

# bot = telebot.TeleBot(settings.TOKEN)

bot.message_handler(commands=['start'])(start)
bot.message_handler()(game_process)

bot.infinity_polling()