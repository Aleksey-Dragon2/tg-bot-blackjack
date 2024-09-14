import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from game import game_func
import telebot
from telebot import types
import config.settings as settings
from game.players import Player

bot = telebot.TeleBot(settings.TOKEN)

players = dict()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Start game')
    markup.row(btn1)
    bot.send_message(message.chat.id, 'Начнем игру?', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Start game' or message.text.lower() == 'restart':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Взять карту')
        btn2 = types.KeyboardButton('Стоп')
        markup.row(btn1, btn2)

        players.setdefault(message.chat.id, Player())
        players[message.chat.id].reset(game_func.get_deck())
        player = players[message.chat.id]
        player.add_user_card(game_func.get_card(player.deck))
        player.add_dealer_card(game_func.get_card(player.deck))
        player.add_user_card(game_func.get_card(player.deck))
        player.add_dealer_card(game_func.get_card(player.deck))

        game_info = f"Карты дилера: {player.dealer_cards[0]}, 🂠\nВаши карты: {player.user_cards}\nСумма карт: {player.user_score}"
        bot.send_message(message.chat.id, game_info, reply_markup=markup)

@bot.message_handler()
def user_add_cart(message):
    if message.chat.id in players:
        player = players[message.chat.id]

        if message.text.lower() == "взять карту":
            player.add_user_card(game_func.get_card(player.deck))
            game_info = f"{player.user_cards}\nСумма карт: {player.user_score}"
            bot.send_message(message.chat.id, game_info)

        elif message.text.lower() == "стоп":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Restart')
            markup.row(btn1)


            while player.dealer_score < 17 and player.user_score < 22:
                player.add_dealer_card(game_func.get_card(player.deck))

            game_info = f"Карты дилера: {player.dealer_cards}\nСумма дилера: {player.dealer_score}\nВаши карты: {player.user_cards}\nСумма карт: {player.user_score}"
            
            if player.user_score > player.dealer_score and player.user_score < 22 or player.dealer_score > 21 and player.user_score < 22:
                bot.send_message(message.chat.id, f"Win,\n{game_info}", reply_markup=markup)
            elif player.user_score < player.dealer_score and player.dealer_score < 22 or player.user_score > 21 and player.dealer_score < 21:
                bot.send_message(message.chat.id, f"lose,\n{game_info}", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, f'ничья,\n{game_info}', reply_markup=markup)

            players.clear()
    elif message.text.lower()=='restart':
        on_click(message)
    else: bot.send_message(message.chat.id, "Игра не зарегестрирована")

bot.infinity_polling()
