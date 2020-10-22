import configparser

from telethon import events
from telethon.sync import TelegramClient
from gpt2bot.api_wrapper import add_attribute_to_knowledge_base

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
    global temperature
    global temperature_decrease_amount
    temperature = temperature - temperature_decrease_amount

    add_attribute_to_knowledge_base('weather_temp', temperature)


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
        print('Loop ' + str(loop_count) + ' completed')
        update_temperature()
        if loop_count < loop_desired_count:
            conversation_state = 'temp_request'
            await client.send_message(bot_username, message1)


message1 = 'What\'s the temperature today?'
message2 = 'Is it freezing?'
message_bye = 'Bye'

temperature = 80
temperature_decrease_amount = 30
loop_desired_count = 5

add_attribute_to_knowledge_base('weather_temp', temperature)

with client:
    send_message(message1)
    client.run_until_disconnected()
