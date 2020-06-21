import argparse
import configparser
import sqlite3
from sqlite3 import Error
import mysql.connector
from deprecated import deprecated
import os

db_sqlite_file = r"database/pythonsqlite.db"

db_username = ''
db_password = ''
db_host = ''
db_dbname = ''


def set_credentials():
    global db_username
    global db_password
    global db_host
    global db_dbname

    # Script arguments can include path of the config
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', type=str, default="gpt2bot/chatbot.cfg")
    args = arg_parser.parse_args()

    config = configparser.ConfigParser(allow_no_value=True)
    config.read("secrets.cfg")
    with open(args.config) as f:
        config.read_file(f)

    db_username = config.get('chatbot', 'db_username')
    db_password = config.get('chatbot', 'db_password')
    db_host = config.get('chatbot', 'db_host')
    db_dbname = config.get('chatbot', 'db_dbname')


@deprecated('MySQL database should be used instead of sqlite')
def create_sqlite_database():
    conn = None
    try:
        conn = sqlite3.connect(db_sqlite_file)

        for sql_statement in os.listdir("database/create_statements"):
            with open("database/create_statements/" + sql_statement) as file:
                query = file.readlines()
                conn.execute(query[0])
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


@deprecated('MySQL database should be used instead of sqlite')
def check_and_prepare_sqlite_database():
    try:
        f = open(db_sqlite_file)
        f.close()  # If file is not found the IOError is thrown before the close
    except IOError:
        create_sqlite_database()


@deprecated('MySQL database should be used instead of sqlite')
def execute_sqlite_query(query, parameter):
    conn = None
    try:
        conn = sqlite3.connect(db_sqlite_file)
        executed_query = conn.execute(query, parameter)
        return executed_query.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


@deprecated('MySQL database should be used instead of sqlite')
def execute_sqlite_query_update(query, parameter):
    conn = None
    try:
        conn = sqlite3.connect(db_sqlite_file)
        conn.execute(query, parameter)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def execute_mysql_select_query(query, parameter):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(user=db_username, password=db_password, host=db_host, database=db_dbname)
        cursor = conn.cursor()

        cursor.execute(query, parameter)

        return cursor.fetchall()

    except Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_mysql_update_query(query, parameter):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(user=db_username, password=db_password, host=db_host, database=db_dbname)
        cursor = conn.cursor()

        cursor.execute(query, parameter)
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_mysql_insert_query(query, parameter):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(user=db_username, password=db_password, host=db_host, database=db_dbname)
        cursor = conn.cursor()

        cursor.execute(query, parameter)
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def check_and_prepare_mysql_database():
    set_credentials()
    conn = None
    try:
        conn = mysql.connector.connect(user=db_username, password=db_password, host=db_host, database=db_dbname)
        print("Connection with MySql database was successful")
    except IOError:
        print("MySql database connection not working")
        raise ConnectionRefusedError
    finally:
        if conn:
            conn.close()


def read_injected_turns():
    injected_turns_array = []
    with open("database/select_statements/read_injected_messages") as select_query_file:
        with open("database/update_statements/update_injected_message_injected") as update_query_file:
            select_query = select_query_file.readlines()[0]
            update_query = update_query_file.readlines()[0]

            # turns = execute_sqlite_query(select_query, (0,))
            turns = execute_mysql_select_query(select_query, ())
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
                    print('Bot -Injected-:' + str(databaseTurn[2]))
                    injected_turns_array.append(turn)
                elif databaseTurn[1] is not None and databaseTurn[2] is None:
                    turn = {
                        'user_messages': [databaseTurn[1]],
                        'bot_messages': []
                    }
                    print('User -Injected-:' + str(databaseTurn[1]))
                    injected_turns_array.append(turn)
                elif databaseTurn[1] is not None and databaseTurn[2] is not None:
                    turn = {
                        'user_messages': [databaseTurn[1]],
                        'bot_messages': [databaseTurn[2]]
                    }
                    print('User -Injected-:' + str(databaseTurn[1]))
                    print('Bot -Injected-:' + str(databaseTurn[2]))
                    injected_turns_array.append(turn)
                execute_mysql_update_query(update_query, (databaseTurn[0],))
    return injected_turns_array


def get_current_chat_id():
    with open("database/select_statements/read_max_chat_id") as select_query_file:
        select_query = select_query_file.readlines()[0]
        max_chat_id = execute_mysql_select_query(select_query, ())
        chat_id = max_chat_id[0][0]
    return chat_id


def insert_chat_history_message(chat_id, sender, injected, message):
    with open("database/insert_statements/insert_chat_history_message") as insert_query:
        query = insert_query.readlines()[0]
        execute_mysql_insert_query(query, (chat_id, sender, injected, message))


def insert_user_profile(key, value):
    with open("database/insert_statements/insert_user_profile") as insert_query:
        query = insert_query.readlines()[0]
        execute_mysql_insert_query(query, (key, value))
