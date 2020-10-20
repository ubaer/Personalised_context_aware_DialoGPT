import configparser

from telethon import events
from telethon.sync import TelegramClient

session_name = 'bot_testing_session'
bot_username = ''
client = TelegramClient

conversation_state = 'temp_request'
loop_count = 0


def initiate_client():
    global bot_username
    global client

    config = configparser.ConfigParser()
    config.read("../secrets.cfg")

    api_id = config.getint('test_environment', 'api_id')
    api_hash = config.get('test_environment', 'api_hash')
    bot_username = config.get('test_environment', 'bot_username')

    client = TelegramClient('anon', api_id, api_hash)


initiate_client()


def send_message(message):
    client.send_message(bot_username, message)


def update_temperature():
    print('todo')


@client.on(events.NewMessage())
async def msg_recieved_handle(event):
    global conversation_state
    global loop_count
    global message_string

    if conversation_state == 'temp_request':
        conversation_state = 'end_request'
        await client.send_message(bot_username, message2)

    elif conversation_state == 'end_request':
        conversation_state = 'end_received'
        await client.send_message(bot_username, message_bye)

    elif conversation_state == 'end_received':
        loop_count = loop_count + 1
        print('Loop ' + loop_count + ' completed')
        update_temperature()
        if loop_count < loop_desired_count:
            conversation_state = 'temp_request'
            await client.send_message(bot_username, message1)


loop_desired_count = 2
message1 = 'What\'s the temperature today?'
message2 = 'Do you consider this hot?'
message_bye = 'Bye'

with client:
    send_message(message1)
    client.run_until_disconnected()
