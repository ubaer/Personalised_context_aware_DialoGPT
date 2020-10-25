import configparser

from telethon import events
from telethon.sync import TelegramClient
from gpt2bot.api_wrapper import add_attribute_to_knowledge_base, save_auto_experiment_chat

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
    global reply_1
    global reply_2

    if conversation_state == 'temp_request':
        conversation_state = 'end_request'
        reply_1 = event.message.message
        await client.send_message(bot_username, message2)

    elif conversation_state == 'end_request':
        conversation_state = 'end_received'
        reply_2 = event.message.message

        await client.send_message(bot_username, message_bye)

    elif conversation_state == 'end_received':
        save_auto_experiment_chat(message1, reply_1, temperature, message2, reply_2)
        print('send request')
        loop_count = loop_count + 1
        print('Loop ' + str(loop_count) + ' completed')
        update_temperature()
        if loop_count < loop_desired_count:
            conversation_state = 'temp_request'
            await client.send_message(bot_username, message1)


message1 = 'What\'s the current temperature?'
message2 = 'Is it freezing?'
reply_1 = ''
reply_2 = ''
message_bye = 'Bye'

temperature = 80
temperature_decrease_amount = 2
loop_desired_count = 2

add_attribute_to_knowledge_base('weather_temp', temperature)

with client:
    send_message(message1)
    client.run_until_disconnected()
