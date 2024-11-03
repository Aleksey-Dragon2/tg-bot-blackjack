import sqlite3
def create_error_log_table():
    connection = sqlite3.connect('error_log.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            error TEXT,
            location_error TEXT,
            last_message TEXT
        )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

def add_error_log(error, location_error, last_message):
    connection = sqlite3.connect('error_log.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO error_log (error, location_error, last_message)
        VALUES (?, ?, ?)
    ''', (error, location_error, last_message))

    connection.commit()
    cursor.close()
    connection.close()

def get_error_log():
    connection = sqlite3.connect('error_log.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM error_log')
    error_log = cursor.fetchall()

    cursor.close()
    connection.close()

    return error_log

def clear_error_log():
    connection = sqlite3.connect('error_log.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM error_log')

    connection.commit()
    cursor.close()
    connection.close()