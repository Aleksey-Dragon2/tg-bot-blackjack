import telebot
from telebot import types
import game_func
import settings

bot = telebot.TeleBot(settings.TOKEN)

players=dict()
deck=game_func.get_deck()
user_cards=list()
dealer_cards=list()
game_info=''
user_score=0
dealer_score=0

@bot.message_handler(commands=['test'])
def start(message):
    player_stats={
        'deck':list(),
        'user_cards':list(),
        'dealer_cards':list(), 
        'game_info':'',
        'user_score':0,
        'dealer_score':0}
    players.setdefault(message.chat.id,player_stats)
    bot.send_message(message.chat.id,players[message.chat.id])


@bot.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1=types.KeyboardButton('Start game')
    markup.row(btn1)

    bot.send_message(message.chat.id,'q', reply_markup=markup)
    bot.register_next_step_handler(message,on_click)

def on_click(message):
    if message.text == 'Start game' or message.text=='Restart':
        global user_score, dealer_score
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1=types.KeyboardButton('Взять карту')
        btn2=types.KeyboardButton('Стоп')
        markup.row(btn1,btn2)
        user_cards.append(game_func.get_card(deck))
        dealer_cards.append(game_func.get_card(deck))
        user_cards.append(game_func.get_card(deck))
        dealer_cards.append(game_func.get_card(deck))

        dealer_score=game_func.summa_cards(dealer_cards)
        user_score=game_func.summa_cards(user_cards)

        game_info=f"Карты диллера:{str(dealer_cards[0])}, 🂠\nВаши карты:{str(user_cards)}\nСумма карт: {user_score}"


        bot.send_message(message.chat.id, game_info ,reply_markup=markup)


    

@bot.message_handler()
def user_add_cart(message):
    if (message.text.lower()=="взять карту"):
        global user_score, dealer_score, dealer_cards, user_cards, deck
        user_cards.append(game_func.get_card(deck))
        user_score=0
        user_score=game_func.summa_cards(user_cards)
        game_info=f"{str(user_cards)}\nСумма карт: {user_score}"
        bot.send_message(message.chat.id,game_info)


    elif (message.text.lower()=="стоп"):
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1=types.KeyboardButton('Restart')
        markup.row(btn1)
        while dealer_score<17 and user_score<22:
            dealer_cards.append(game_func.get_card(deck))
            dealer_score=game_func.summa_cards(dealer_cards)
        game_info=f"Карты диллера:{str(dealer_cards)},\nСумма диллера:{dealer_score}\nВаши карты:{str(user_cards)}\nСумма карт: {user_score}"
        if user_score>dealer_score and user_score<22 or 21<dealer_score and user_score<22:
            bot.send_message(message.chat.id,f"Win,\n{game_info}",reply_markup=markup)
        elif user_score<dealer_score and dealer_score<22 or user_score>21 and dealer_score<21:
            bot.send_message(message.chat.id,f'lose,\n{game_info}',reply_markup=markup) ## Сделать условие
        else:
            bot.send_message(message.chat.id,f'ничья,\n{game_info}',reply_markup=markup)

        user_score=0
        dealer_score=0
        user_cards.clear()
        dealer_cards.clear()
        deck.clear()
        deck=game_func.get_deck()
    bot.register_next_step_handler(message,on_click)



bot.infinity_polling()