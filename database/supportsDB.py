import sqlite3
def create_support_table():
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relevant_support (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            username TEXT,
            name TEXT NOT NULL,
            text TEXT,
            status TEXT DEFAULT 'Active'
        )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

def get_support_user_id(support_id):
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()

    cursor.execute('''
                SELECT user_id FROM relevant_support WHERE id=?;
                ''', (support_id,))
    support=cursor.fetchall()
    user_id=support[0][0]

    connection.commit()
    cursor.close()
    connection.close()

    return user_id

def add_support_message(user_id, username, name, text):
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO relevant_support (user_id, username, name, text)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, name, text))

    connection.commit()
    cursor.close()
    connection.close()
    

def check_support_messages():
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()

    cursor.execute('''
                SELECT id, 
                DATETIME(time, '+3 hours') AS time, 
                text
                FROM relevant_support;
                ''')
    supports=cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()
    return supports

def get_all_support_message_user(user_id):
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()

    cursor.execute('''
                SELECT 
                id,
                DATETIME(time, '+3 hours') AS time,
                name, 
                text,
                "В очереди" AS explanation,
                status
                FROM relevant_support
                WHERE user_id=?
                   
                UNION ALL
                   
                SELECT 
                id,
                DATETIME(time, '+3 hours') AS time,
                name, 
                text,
                explanation,
                status
                FROM archive_support
                WHERE user_id=?;
                ''', (user_id, user_id))
    supports=cursor.fetchall()
    cursor.close()
    connection.close()

    return supports

def check_support_message_by_id(support_id):
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()

    cursor.execute('''
                SELECT
                id,
                DATETIME(time, '+3 hours') AS time,
                user_id,
                username, 
                name, 
                text,
                status
                FROM relevant_support 
                WHERE id=?;
                ''', (support_id,))
    supports=cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()
    return supports
    
def get_all_support_ids():
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()


    cursor.execute("SELECT id FROM relevant_support")
    

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return [user[0] for user in users]

def clear_support_message():
    conn = sqlite3.connect('supports.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM relevant_support")

    conn.commit()
    cursor.close()
    conn.close()