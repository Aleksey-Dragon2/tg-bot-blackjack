from game.players import Player
from bot.markup import start_markup, game_markup, restart_markup, support_markup
import game.deck as deck
from bot.common import bot
import config.language as lang
import bot.database as db
from config.settings import SUPERUSERS
import bot.admin_commands as admin

players=dict()




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
    
    elif message.text.lower()==lang.stats.lower():
        send_stats(message)
        print(message.from_user.id)
        
    elif message.text.lower()==lang.superuser.lower() and message.from_user.id in SUPERUSERS:
        admin.superuser(message)

    elif message.text.lower()==lang.all_users.lower() and message.from_user.id in SUPERUSERS:
        admin.check_stats(message)

    elif message.text.lower()==lang.support_menu.lower():
        support_menu(message)

    elif message.text.lower()==lang.send_support_message.lower():
        send_support_message(message)

    elif message.text.lower()=='delete' and message.from_user.id in SUPERUSERS:
        db.delete_user('')

    elif message.text.lower()==lang.admin_support.lower() and message.from_user.id in SUPERUSERS:
        admin.check_all_supports(message)
    
    elif message.text.lower()==lang.support_back.lower():
        start(message)
    
    elif message.text.lower()==lang.send_message_all.lower():
        get_message_to_send(message)

    else: #not player and message.text.lower() !=lang.restart.lower():
        check_register_game(message,player)


def start(message):
    db.create_user_table()
    db.create_support_table()
    db.add_user(message)
    bot.send_message(message.chat.id, lang.FIRST_MESSAGE, reply_markup=start_markup(), parse_mode='HTML')
    # bot.send_message(message.chat.id, lang.FIRST_MESSAGE, reply_markup=test_markuo(), parse_mode='HTML')

# @bot.callback_query_handler(func=lambda callback:True)
# def callback_message(callback):
#     if callback.data=='start game':
#         bot.edit_message_text("Edit text",callback.message.chat.id,callback.message.message_id)


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


def user_move(message,player):
    player.add_user_card(deck.get_card(player.deck))
    check_game_status(message,player)


def send_game_rules(message):
    bot.send_message(message.chat.id,lang.GAME_RULES)


def check_register_game(message,player):
    bot.send_message(message.chat.id,lang.GAME_NOT_REGISTER)


def dealer_move(message, player):
    while player.dealer_score < 17 and player.user_score < 22 and player.user_score>player.dealer_score:
        player.add_dealer_card(deck.get_card(player.deck))
    finalize_game(message, player)
    

def send_game_status(message,player):
    game_info=lang.GAME_INFO(player)   
    bot.send_message(message.chat.id,game_info,reply_markup=game_markup(), parse_mode='HTML')


def check_game_status(message,player):
    if player.user_score>=21:
            finalize_game(message,player)
    else:
        send_game_status(message,player)


def finalize_game(message,player):
    user_id=message.from_user.id
    result=deck.calculate_result(player,user_id)
    bot.send_message(message.chat.id, result, reply_markup=restart_markup(), parse_mode="HTML")
    players.clear()

def send_stats(message):
    user_stats=lang.GET_USER_STATS(message.from_user.id)
    bot.send_message(message.chat.id,user_stats, parse_mode='HTML')

def support_menu(message):
    bot.send_message(message.chat.id,lang.HELP_SUPPORT,reply_markup=support_markup())

def send_support_message(message):
    bot.send_message(message.chat.id,"Отправьте ваше сообщение:")
    bot.register_next_step_handler(message,add_support_message)

def add_support_message(message):
    user_id = message.from_user.id
    username =message.from_user.username
    name = message.from_user.first_name
    db.add_support_message(user_id,username,name,message.text)
    bot.send_message(message.chat.id,"Ваше сообщение передано!")
    start(message)

def get_message_to_send(message):
    bot.send_message(message.chat.id,"Отправьте ваше сообщение")
    bot.register_next_step_handler(message, send_message_to_all_user)

def send_message_to_all_user(message):
    if message.from_user.id in SUPERUSERS:

        users=db.get_users_ids()
        for user_id in users:
            bot.send_message(user_id, message.text)



    # bot.send_message(1147113777,message.text)
    # bot.send_message(1070684527, message.text)