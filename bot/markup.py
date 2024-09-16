from telebot import types
import config.language as lang
def start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(lang.start_game)
    btn2=types.KeyboardButton(lang.markup_rules)
    btn3=types.KeyboardButton(lang.stats)
    markup.row(btn1)
    markup.row(btn3,btn2)
    return markup

def game_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1=types.KeyboardButton(lang.get_card)
    btn2=types.KeyboardButton(lang.stop)
    markup.row(btn1,btn2)
    return markup

def restart_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(lang.restart)
    btn2 = types.KeyboardButton(lang.main)
    markup.row(btn1,btn2)
    return markup