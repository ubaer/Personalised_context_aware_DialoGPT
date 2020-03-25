import sqlite3
from sqlite3 import Error
import os

db_file = r"database/pythonsqlite.db"


def create_database():
    conn = None
    try:
        conn = sqlite3.connect(db_file)

        for sql_statement in os.listdir("database/create_statements"):
            with open("database/create_statements/" + sql_statement) as file:
                query = file.readlines()
                conn.execute(query[0])
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def check_and_prepare_database():
    try:
        f = open(db_file)
        f.close()  # If file is not found the IOError is thrown before the close
    except IOError:
        create_database()


def execute_query(query, parameter):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        executed_query = conn.execute(query, parameter)
        return executed_query.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def execute_query_update(query, parameter):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute(query, parameter)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def read_injected_turns():
    injected_turns_array = []
    with open("database/select_statements/read_injected_messages") as select_query_file:
        with open("database/update_statements/update_injected_message_injected") as update_query_file:
            select_query = select_query_file.readlines()[0]
            update_query = update_query_file.readlines()[0]

            turns = execute_query(select_query, (0,))
        if (len(turns) > 0):
            for databaseTurn in turns:
                if databaseTurn[1] is None and databaseTurn[2] is None:
                    turn = {
                        'user_messages': [],
                        'bot_messages': []
                    }
                    injected_turns_array.append(turn)
                elif databaseTurn[1] is None and databaseTurn[2] is not None:
                    turn = {
                        'user_messages': [],
                        'bot_messages': [databaseTurn[2]]
                    }
                    injected_turns_array.append(turn)
                elif databaseTurn[1] is not None and databaseTurn[2] is None:
                    turn = {
                        'user_messages': [databaseTurn[1]],
                        'bot_messages': []
                    }
                    injected_turns_array.append(turn)
                execute_query_update(update_query, (databaseTurn[0],))
    return injected_turns_array
