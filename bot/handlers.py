from telebot import types
from game.players import Player
import bot.messages as messages
from bot.markup import start_markup,game_markup, restart_markup
import game.deck as deck
from bot.common import bot
import config.language as lang

players=dict()

def start(message):
    bot.send_message(message.chat.id, lang.first_message, reply_markup=start_markup())

def game_start(message):
        player=initialization_player(message.from_user.id)
        check_game_status(message,player)

def initialization_player(chat_id):
    players[chat_id]=Player()
    players[chat_id].reset(deck.get_deck())
    player=players[chat_id]

    player.add_user_card(deck.get_card(player.deck))
    player.add_dealer_card(deck.get_card(player.deck))
    player.add_user_card(deck.get_card(player.deck))
    player.add_dealer_card(deck.get_card(player.deck))
    
    return player

def register_handlers(message):
    player=players.get(message.from_user.id)
    if message.text.lower()==lang.get_card.lower():
        user_move(message,player)

    elif message.text.lower() == lang.start_game.lower() or message.text.lower() == lang.restart.lower():
         game_start(message)

    elif message.text.lower()==lang.stop.lower():
        dealer_move(message,player)

    elif message.text.lower()==lang.restart.lower():
        game_start(message)

    elif message.text.lower()==lang.markup_rules.lower():
        send_game_rules(message)

    elif message.text.lower()==lang.main.lower():
        start(message)
    
    else: #not player and message.text.lower() !=lang.restart.lower():
        check_register_game(message,player)



def user_move(message,player):
    player.add_user_card(deck.get_card(player.deck))
    check_game_status(message,player)

def send_game_rules(message):
    bot.send_message(message.chat.id,lang.game_rules)


def check_register_game(message,player):
    bot.send_message(message.chat.id,messages.GAME_NOT_REGISTER)


def dealer_move(message, player):
    while player.dealer_score < 17 and player.user_score < 22 and player.user_score>player.dealer_score:
        player.add_dealer_card(deck.get_card(player.deck))
    finalize_game(message, player)
    

def send_game_status(message,player):
        game_info = (f"Карты дилера: {player.dealer_cards[0]}, 🂠\n"
                     f"Ваши карты: {player.user_cards}\n"
                     f"Сумма карт: {player.user_score}")
        bot.send_message(message.chat.id,game_info,reply_markup=game_markup())


def check_game_status(message,player):
    if player.user_score>=21:
            finalize_game(message,player)
    else:
        send_game_status(message,player)


def finalize_game(message,player):
    result=deck.calculate_result(player)
    bot.send_message(message.chat.id, result, reply_markup=restart_markup())
    players.clear()
