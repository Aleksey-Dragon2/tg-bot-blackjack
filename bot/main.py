import telebot
from bot.handlers import *
import config.settings
from bot.common import bot

# bot = telebot.TeleBot(settings.TOKEN)

bot.message_handler(commands=['start'])(start)
bot.message_handler()(register_handlers)

bot.infinity_polling()