import sqlite3
def create_archive_support_table():
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archive_support (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            username TEXT,
            name TEXT NOT NULL,
            text TEXT,
            explanation TEXT DEFAULT 'No',
            status TEXT DEFAULT 'Closed'
        )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

def move_support_to_archive(support_id, status):
    support_conn = sqlite3.connect('supports.db')

    try:
        support_cursor = support_conn.cursor()

        support_conn.execute('BEGIN')


        support_cursor.execute('''
            INSERT INTO archive_support (id, time, user_id, username, name, text, status)
            SELECT id, time, user_id, username, name, text, ?
            FROM relevant_support
            WHERE id = ?
        ''', (status,support_id,))

        support_cursor.execute('DELETE FROM relevant_support WHERE id = ?', (support_id,))

        support_conn.commit()

    except sqlite3.Error as e:
        support_conn.rollback()
        print(f"Ошибка при перемещении записи: {e}")

    finally:
        support_conn.close()


def check_archive_support_messages():
    connection = sqlite3.connect('supports.db')
    cursor = connection.cursor()

    cursor.execute('''
                SELECT id, 
                DATETIME(time, '+3 hours') AS time, 
                user_id, 
                username, 
                name, 
                text,
                explanation,
                status
                FROM archive_support
                ''')
    supports=cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()
    return supports

def check_archive_support_message_by_id(support_id):
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
                explanation,
                status
                FROM archive_support 
                WHERE id=?;
                ''', (support_id,))
    supports=cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()
    return supports

