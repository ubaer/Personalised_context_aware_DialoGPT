import argparse

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from telegram.ext import Updater
from database.database_wrapper import execute_mysql_insert_query, set_credentials, get_current_chat_id, \
    insert_chat_history_message

import configparser

app = FlaskAPI(__name__)


@app.route("/avg_volume/", methods=['GET', 'POST'])
def add_avg_volume():
    if request.method == 'POST':
        with open("database/insert_statements/insert_volume_table") as insert_query:
            avg_amplitude = int(request.data.get('amplitude', ''))
            avg_decibel = int(request.data.get('decibel', ''))

            set_credentials()
            query = insert_query.readlines()[0]
            execute_mysql_insert_query(query, (avg_amplitude, avg_decibel))

    return ""


@app.route("/inject_message/", methods=['GET', 'POST'])
def add_inject_message():
    global current_chat_id
    if request.method == 'POST':
        with open("database/insert_statements/insert_inject_table") as insert_query:
            user_message = request.data.get('user_message', '')
            if user_message == "":
                user_message = None
            else:
                insert_chat_history_message(current_chat_id, 'user', '1', user_message)

            bot_message = request.data.get('bot_message', '')
            if bot_message == "":
                bot_message = None
            else:
                insert_chat_history_message(current_chat_id, 'bot', '1', bot_message)
                updater.bot.send_message(chat_id=active_telegram_chat_id, text=bot_message)

            set_credentials()
            query = insert_query.readlines()[0]
            execute_mysql_insert_query(query, (user_message, bot_message))

    return ""


@app.route("/new_chat/", methods=['GET'])
def new_conversation():
    global current_chat_id
    if request.method == 'GET':
        set_credentials()
        current_chat_id = get_current_chat_id() + 1
        print(current_chat_id)
    return {'chat_id': current_chat_id}


@app.route("/add_message_to_history/", methods=['GET', 'POST'])
def add_message_to_history():
    global current_chat_id
    if request.method == 'POST':
        sender = request.data.get('sender', '')
        injected = request.data.get('injected', '')
        message = request.data.get('message', '')
        insert_chat_history_message(current_chat_id, sender, injected, message)
    return ""


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', type=str, default="gpt2bot/chatbot.cfg")
    args = arg_parser.parse_args()
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("secrets.cfg")
    with open(args.config) as f:
        config.read_file(f)

    updater = Updater(token=config.get('chatbot', 'telegram_token'), use_context=True)
    active_telegram_chat_id = config.get('chatbot', 'active_chat_id')

    set_credentials()
    current_chat_id = get_current_chat_id()
    # setting host is required to publish the API to your local network
    app.run(debug=True, host='0.0.0.0')
