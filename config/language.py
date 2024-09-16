from game.players import Player
import bot.database as db
##     \ buttons+game logic /    ##
# start_game='Start game'
# restart='Restart'
# get_card='Get card'
# stop='Stop'
# markup_rules='Rules'
# main='Main page

###     \ Messages to the user /    ##
# first_message='Start the game?'

###     \ Markups /    ##


##     \ Кнопки+игровая логика /    ##
start_game='Начать игру🎮'
restart='Сыграть еще раз🔁'
get_card='Взять карту🃏'
stop='Стоп🚫'
markup_rules='Правила🎟'
main='Главная📄'
stats='Статистика'

##     \ Сообщения пользователю /    ##
first_message=('Привет!\n' 
            'Со мной вы можете поиграть в <b>блэкджек.</b>🍾\n'
            'Ознакомьтесь с правилами или сразу начинайте игру!🃏'
            )

game_rules =(   "🃏🎲 Правила игры в Блэкджек:\n\n"
                '1.🎯 Цель игры — набрать 21 очко или ближе к этому,  не превышая 21.\n'
                '2.🃏 Карты на руках: Игрок и дилер получают по 2 карты. Игрок видит обе свои карты, дилер — только одну из своих.\n'
                '3.🂠 Очки карт: Туз — 1 или 11 очков (выгоднее для игрока). Карты с 2 по 10 — номинал карты. Король, Дама, Валет — по 10 очков.\n'
                '4.👤 Действия игрока: Взять карту (Hit) — добавить ещё одну карту. Остаться (Stand) — завершить ход.\n'
                '5.❌ Перебор: Если сумма очков больше 21 — это перебор, и игрок проигрывает.\n'
                '6.🔄 Ход дилера: Когда игрок завершает ход, дилер открывает вторую карту и продолжает брать карты до 17 очков.\n'
                '7.🏆 Победа: Побеждает тот, у кого сумма очков ближе к 21, но не больше.\n'
                )

def get_user_stats(user_id):
    stats=db.get_user_stats(user_id)
    user_stats=(f"{stats['name']}, ваша статистика:\n\n"
                f"Побед: {stats['wins']}\n"
                f"Поражений: {stats['losses']}\n"
                f"Всего игр: {stats['games']}"
                )
    return user_stats

def game_info(player):
    game_info = (   f"<b>Ход игрока.</b>\n\n"
                    f"<b>Карты дилера:</b> {player.dealer_cards[0]}, 🂠\n"
                    f"<b>Ваши карты:</b> {', '.join(player.user_cards)}.\n\n"
                    f"<b>Сумма карт:</b> {player.user_score}"
                    )
    return game_info

##     \ Кнопки /    ##
