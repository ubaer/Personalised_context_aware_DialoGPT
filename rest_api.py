from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from database.database_wrapper import execute_mysql_insert_query, set_credentials

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
    if request.method == 'POST':
        with open("database/insert_statements/insert_inject_table") as insert_query:
            user_message = request.data.get('user_message', '')
            if user_message == "":
                user_message = None

            bot_message = request.data.get('bot_message', '')
            if bot_message == "":
                bot_message = None

            set_credentials()
            query = insert_query.readlines()[0]
            execute_mysql_insert_query(query, (user_message, bot_message))

    return ""


if __name__ == "__main__":
    # setting host is required to publish the API to your local network
    app.run(debug=True, host='0.0.0.0')
