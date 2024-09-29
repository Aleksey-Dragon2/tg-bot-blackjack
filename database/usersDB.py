import sqlite3


def create_user_table():
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
    username =message.from_user.username
    name = message.from_user.first_name

    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("INSERT INTO users (id, username, name) VALUES (?, ?, ?)",
                       (user_id, username, name))
        connection.commit()

    cursor.close()
    connection.close()

def add_user_id(user_id, username, name):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("INSERT INTO users (id, username, name) VALUES (?, ?, ?)",
                       (user_id, username, name))
        connection.commit()

    cursor.close()
    connection.close()
    



def delete_user(user_id):
    conn = sqlite3.connect('users.db') 
    cursor = conn.cursor()


    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()


    conn.close()


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


def get_user_by_id(user_id):
    conn=sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, name, wins, losses, games FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


def get_user_stats(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()


    cursor.execute("SELECT id, name, wins, losses, games FROM users WHERE id = ?", (user_id,))
    
    stats = cursor.fetchone()

    cursor.close()
    connection.close()

    if stats is not None:
        id, name, wins, losses, games = stats
        return {
            "id":id,
            "name": name,
            "wins": wins,
            "losses": losses,
            "games": games
        }
    else:
        return None
    
def get_rating_users():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("SELECT name, wins FROM users ORDER BY wins DESC LIMIT 3")
    top_users = cursor.fetchall()

    cursor.close()
    connection.close()

    return top_users

def get_users_rating_by_id(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("""
                    SELECT COUNT(*) + 1 AS position
                    FROM users
                    WHERE wins > (SELECT wins FROM users WHERE id = ?)
                """, 
                (user_id,))

    position = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return position

def clear_user_stats(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE users 
                      SET wins = 0, losses = 0, games = 0 
                      WHERE id = ?''', (user_id,))
    connection.commit()
    connection.close()


def get_users_ids():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users")
    rows = cursor.fetchall()

    id_list = [row[0] for row in rows]


    conn.close()

    return id_list


