import bot.database as db
from aiogram.fsm.context import FSMContext

##     \ buttons+game logic /    ##
# start_game='Start game'
# restart='Restart'
# get_card='Get card'
# stop='Stop'
# markup_rules='Rules'
# main='Main page

###     \ Messages to the user /    ##
# FIRST_MESSAGE='Start the game?'



##     \ Кнопки+игровая логика /    ##

START_GAME='Начать игру🎮'
RESTART='Сыграть еще раз🔁'
GET_CARD=('Взять карту🃏', 'Взять карту')
STOP=('Стоп🚫', 'Стоп')
RULES=('Правила🎟', 'Правила')
MAIN=('Главная📄', 'Главная')
STATS=('Статистика📊', 'Статистика')
SUPPORT=('Поддержка❓', 'Поддержка')
SUPPORT_BACK=('Назад', 'Отмена')
SEND_SUPPORT_MESSAGE=('Отправить сообщение', 'сообщение')
CONFIRM_SUPPORT_MESSAGE=('Да, все верно', 'Да')
DENY_SUPPORT_MESSAGE=('Нет, неверно', 'Нет')
##     \ Сообщения пользователю /    ##

GAME_INVALID_MOVE="Пожалуйста, выберите 'Взять карту' или 'Стоп' для продолжения игры."
COMMAND_NOT_FOUND="Команда не распознана, возвращаю вас на главную"

HELP_SUPPORT='Для отправки вашей жалобы или предложения по улучшению нажмите "Отправить сообщение".\n'
SUPPORT_MESSAGE='Введите ваше сообщение'
SUPPORT_INVALID_MOVE='Пожалуйста, выберите "Отправить сообщение" или "Отмена"'

WIN_GAME='<b>🏆Победа!🏆</b>'
LOSE_GAME='<b>Поражение</b>'
DRAW_GAME='<b>Ничья</b>'

FIRST_MESSAGE=('Привет!\n' 
            'Со мной вы можете поиграть в <b>блэкджек.</b>🍾\n'
            'Ознакомьтесь с правилами или сразу начинайте игру!🃏'
            )

def SUPPORT_MESSAGE_CONFIRMATION(text):
    return f'Ваше сообщение: "{text}", все верно?'

def SUPPORT_MESSAGE_SENT(text):
    return f'Сообщение "{text}" отправлено'

def SUPPORT_MESSAGE_DENIED(text):
    return f'Сообщение "{text}" отклонено'


RULES_TEXT =(   "🃏🎲 Правила игры в Блэкджек:\n\n"
                '1.🎯 Цель игры — набрать 21 очко или ближе к этому,  не превышая 21.\n'
                '2.🃏 Карты на руках: Игрок и дилер получают по 2 карты. Игрок видит обе свои карты, дилер — только одну из своих.\n'
                '3.🂠 Очки карт: Туз — 1 или 11 очков (выгоднее для игрока). Карты с 2 по 10 — номинал карты. Король, Дама, Валет — по 10 очков.\n'
                '4.👤 Действия игрока: Взять карту (Hit) — добавить ещё одну карту. Остаться (Stand) — завершить ход.\n'
                '5.❌ Перебор: Если сумма очков больше 21 — это перебор, и игрок проигрывает.\n'
                '6.🔄 Ход дилера: Когда игрок завершает ход, дилер открывает вторую карту и продолжает брать карты до 17 очков.\n'
                '7.🏆 Победа: Побеждает тот, у кого сумма очков ближе к 21, но не больше.\n'
                )

def GET_USER_STATS(user_id):
    stats=db.get_user_stats(user_id)
    if stats is not None:
        user_stats=(f"<b>{stats['name']}, ваша статистика:</b>\n\n"
                    f"Побед🏅: {stats['wins']}\n"
                    f"Поражений🪦: {stats['losses']}\n"
                    f"Всего игр🕹️: {stats['games']}"
                    )
    else:
        user_stats=f"Пока нет статистики"
    return user_stats

async def GAME_INFO(player, state: FSMContext):
    data = await state.get_data()
    game_info = (   f"<b>Ход игрока.</b>\n\n"
                    f"<b>Карты дилера:</b> {data['dealer_cards'][0]}, 🂠\n"
                    f"<b>Ваши карты:</b> {', '.join(data['user_cards'])}.\n\n"
                    f"<b>Сумма карт:</b> {data['user_score']}"
                    )
    return game_info

def GAME_RESULT(user_cards, dealer_cards, user_score, dealer_score):
    game_info = (
                    f"<b>Карты дилера:</b> {', '.join(dealer_cards)}.\n"
                    f"<b>Сумма дилера:</b> {dealer_score}.\n"
                    f"<b>Ваши карты:</b> {', '.join(user_cards)}.\n\n"
                    f"<b>Сумма карт:</b> {user_score}"
                    )
    return game_info

##     \ Кнопки+логика администратора /    ##
SUPERUSER=('admin', 'админ', '/admin')
ALL_USERS='Все пользователи'
ADMIN_SUPPORT='Список предложений'
ADMIN_SUPPORT_RESET='Очистить предложения'
SEND_MESSAGE_ALL='Сообщить всем'
CONFIRM_SEND_MESSAGE_ALL='Подтвердить'
DENY_SEND_MESSAGE_ALL='Отменить'

##     \ Сообщения администратору /    ##
ADMNIN_PANEL="Добро пожаловать в админ панель."
def check_all_supports():
    supports=db.check_support_message()
    if supports:
        support_list=''
        for support in supports:
            id, time, user_id, username, name, text = support
            support_list+=f"ID: {id}, Time:{time}, User_id: {user_id}, Username: {username}, Name: {name}, Text: {text}\n"
        return f"Список предложений:\n{support_list}"
    else:
        return "Нет предложений"

def check_all_users():
    users=db.get_users()
    if users:
        user_list=''
        for user in users:
            user_id, username, name, wins, losses, games = user
            user_list += f"ID: {user_id}, Username: {username}, Name: {name}, Wins: {wins}, Losses: {losses}, Games: {games}\n"
        return f"Список пользователей:\n{user_list}"
    else:
        return "Нет пользователей"

def SEND_MESSAGE_ALL_CONFIRMATION(text):
    return f'Вы уверены, что хотите отправить это сообщение всем пользователям?\n\n{text}'

def SEND_MESSAGE_ALL_SENT(text):
    return f'Сообщение "{text}" отправлено всем пользователям'

def SEND_MESSAGE_ALL_DENIED(text):
    return f'Сообщение "{text}" отклонено'

