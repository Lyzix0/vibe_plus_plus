import sqlite3

connection = sqlite3.connect('user_db.db')


def add_user(user_id: int, name: str):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users(user_id, name) VALUES (?, ?)',
                   (user_id, name,))
    connection.commit()


def has_user(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id=?',
                   (user_id,))
    return cursor.fetchone()
