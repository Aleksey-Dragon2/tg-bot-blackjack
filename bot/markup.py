from telebot import types

def start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Start game')
    markup.row(btn1)
    return markup

def game_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1=types.KeyboardButton('Взять карту')
    btn2=types.KeyboardButton('Стоп')
    markup.row(btn1,btn2)
    return markup

def restart_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Restart')
    markup.row(btn1)
    return markup