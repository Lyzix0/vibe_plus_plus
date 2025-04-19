import sqlite3
import os

DB_FILE = 'user_db.db'


def init_db():
    db_exists = os.path.exists(DB_FILE)

    con = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = con.cursor()

    if not db_exists:
        print(f"Создаем новую базу данных в файле {DB_FILE}")
        cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        ''')
        con.commit()
        print("Таблица 'users' успешно создана")
    else:
        print(f"База данных {DB_FILE} уже существует")


if __name__ != "__main__":
    init_db()
    connection = sqlite3.connect(DB_FILE)


def add_user(user_id: int, name: str):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users(user_id, name) VALUES (?, ?)',
                   (user_id, name))
    connection.commit()


def user_data(user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id=?',
                   (user_id,))
    return cursor.fetchone()

