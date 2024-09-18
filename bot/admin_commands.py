from bot.common import bot
import config.language as lang
import bot.database as db
import bot.markup as markup
    

def superuser(message):
    bot.send_message(message.chat.id, lang.ADMNIN_PANEL, reply_markup=markup.superuser_markup())

def check_stats(message):
    users=db.get_users()
    if users:
        user_list=''
        for user in users:
            user_id, username, name, wins, losses, games = user
            user_list += f"ID: {user_id}, Username: {username}, Name: {name}, Wins: {wins}, Losses: {losses}, Games: {games}\n"
        bot.send_message(message.chat.id, f"Зарегистрированные пользователи:\n{user_list}")
    else:
        bot.send_message(message.chat.id, "Нет зарегистрированных пользователей.")

def check_all_supports(message):
    supports=db.check_support_message()
    if supports:
        support_list=''
        for support in supports:
            user_id, username, name, text = support
            support_list+=f"ID: {user_id}, Username: {username}, Name: {name}, Text: {text}\n"
        bot.send_message(message.chat.id, f"Список сообщений:\n{support_list}")
    else:
        bot.send_message(message.chat.id,"Нет сообщений")