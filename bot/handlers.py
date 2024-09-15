from telebot import types
from game.players import Player
import bot.messages as messages
from markup import start_markup,game_markup, restart_markup
import deck
from common import bot

players=dict()

def start(message):
    bot.send_message(message.chat.id, 'Начнем игру?', reply_markup=start_markup())
    bot.register_next_step_handler(message, game_start)

def game_start(message):
    if message.text == 'Start game' or message.text.lower() == 'restart':
        player=initialization_player(message.chat.id)
        send_game_status(message,player)

def initialization_player(chat_id):
    players[chat_id]=Player()
    players[chat_id].reset(deck.get_deck())
    player=players[chat_id]

    player.add_user_card(deck.get_card(player.deck))
    player.add_dealer_card(deck.get_card(player.deck))
    player.add_user_card(deck.get_card(player.deck))
    player.add_dealer_card(deck.get_card(player.deck))
    
    return player

def game_process(message):
    player=players.get(message.chat.id)
    if not player and message.text.lower() !='restart':
        bot.send_message(message.chat.id,messages.GAME_NOT_REGISTER)
    if message.text.lower()=='взять карту':
            player.add_user_card(deck.get_card(player.deck))
            if player.user_score>21:
                 finalize_game(message,player)
            else:
                send_game_status(message,player)
    elif message.text.lower()=='стоп':
        while player.dealer_score < 17 and player.user_score < 22 and player.user_score>=player.dealer_score:
            player.add_dealer_card(deck.get_card(player.deck))
        finalize_game(message, player)

    elif message.text.lower()=='restart':
        game_start(message)


def send_game_status(message,player):
        game_info = (f"Карты дилера: {player.dealer_cards[0]}, 🂠\n"
                     f"Ваши карты: {player.user_cards}\n"
                     f"Сумма карт: {player.user_score}")
        bot.send_message(message.chat.id,game_info,reply_markup=game_markup())

def finalize_game(message,player):
    result=deck.calculate_result(player)
    bot.send_message(message.chat.id, result, reply_markup=restart_markup())
    players.clear()
