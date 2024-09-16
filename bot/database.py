import sqlite3

def create_table():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        name TEXT NOT NULL,
                        wins INTEGER DEFAULT 0,
                        losses INTEGER DEFAULT 0,
                        games INTEGER DEFAULT 0
                    )''')

    connection.commit()
    cursor.close()
    connection.close()

def add_user(message):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    user_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name

    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("INSERT INTO users (id, username, name) VALUES (?, ?, ?)",
                       (user_id, username, name))
        connection.commit()

    cursor.close()
    connection.close()


def get_users():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()


    cursor.execute("SELECT * FROM users")
    

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users

def add_win(user_id): ## message.from_user.id
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET wins = wins + 1, games = games + 1 WHERE id = ?", (user_id,))
    
    connection.commit()
    cursor.close()
    connection.close()

def add_lose(user_id): ## message.from_user.id
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET losses = losses + 1, games = games + 1 WHERE id = ?", (user_id,))
    
    connection.commit()
    cursor.close()
    connection.close()

def add_game(user_id): ## message.from_user.id
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET games = games + 1 WHERE id = ?", (user_id,))
    
    connection.commit()
    cursor.close()
    connection.close()


def get_user_stats(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()


    cursor.execute("SELECT name, wins, losses, games FROM users WHERE id = ?", (user_id,))
    
    stats = cursor.fetchone()

    cursor.close()
    connection.close()

    if stats is not None:
        name, wins, losses, games = stats
        return {
            "name": name,
            "wins": wins,
            "losses": losses,
            "games": games
        }
    else:
        return None