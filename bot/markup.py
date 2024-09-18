from telebot import types
import config.language as lang
import bot.database as db

def start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(lang.start_game)
    btn2=types.KeyboardButton(lang.markup_rules)
    btn3=types.KeyboardButton(lang.stats)
    btn4=types.KeyboardButton(lang.support)
    markup.row(btn1,btn3)
    markup.row(btn2,btn4)
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
    markup.row(btn1)
    markup.row(btn2)
    return markup

def support_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(lang.send_support_message)
    btn2 = types.KeyboardButton(lang.support_back)
    markup.row(btn1,btn2)
    return markup

def superuser_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(lang.all_users)
    markup.row(btn1)
    return markup