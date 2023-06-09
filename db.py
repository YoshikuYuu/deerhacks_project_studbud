import sqlite3
import json
from datetime import datetime

def initialize_db() -> tuple:
    # Following code makes a database with user, task, and time
    # Store time as datetime object if possible?
    # id is datetime.datetime.now
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY NOT NULL,
                        tasks TEXT DEFAULT '{}',
                        points INT DEFAULT 0)''')
    return conn, cursor

def user_in_db(cursor, user_id) -> bool:
    """ Check if a user is already in the database."""
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result

def add_user_to_db(cursor, conn, user_id):
    cursor.execute("INSERT INTO users (user_id, tasks) VALUES (?, '')", (user_id,))
    conn.commit()

    # close database connection
    # cursor.close()
    # conn.close()

def get_user_tasks(cursor, user_id) -> dict:
    cursor.execute("SELECT tasks FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result == ('',):
        user_tasks = {}
    else:
        user_tasks = json.loads(result[0])
    return user_tasks

def add_task(cursor, conn, user_id, task, time_formatted):
    """ Loads user data from SQL db, converts it into a dict, adds a dict item,
    converts the updated dict back into SQL, and updates the db."""
    current_tasks = get_user_tasks(cursor, user_id)
    current_tasks[task] = time_formatted
    print(current_tasks)
    cursor.execute("UPDATE users SET tasks=? WHERE user_id=?", (json.dumps(current_tasks), user_id))
    conn.commit()

def delete_task(cursor, conn, user_id, task_name):
    """ Loads user data SQL db, converts it into a dict, removes a dict item,
    converts updated back into SQL, and updaes the db."""
    current_tasks = get_user_tasks(cursor, user_id)
    if current_tasks != {}:
        current_tasks.pop(task_name)
        print(current_tasks)
        cursor.execute("UPDATE users SET tasks=? WHERE user_id=?", (json.dumps(current_tasks), user_id))
        conn.commit()

def db_get_tasks_time(cursor, time):
    """ Returns a list of tuples containing (user_id, task) that match the
    given time."""
    cursor.execute("SELECT user_id, tasks FROM users")
    values = cursor.fetchall()
    matching_tasks = []
    for value in values:
        user_id = value[0]
        tasks = json.loads(value[1])
        print(tasks)
        for task in tasks:
            if tasks[task] == time:
                matching_tasks.append((user_id, task))
    return matching_tasks


def add_points(cursor, p: int, user_id):
    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (p, user_id))


def get_points(cursor, user_id):
    cursor.execute('SELECT points FROM users WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    return int(result[0])


def display_values(cursor, user_id):
    cursor.execute("SELECT tasks FROM users WHERE user_id=?", (user_id,))
    values = cursor.fetchone()
    return values
