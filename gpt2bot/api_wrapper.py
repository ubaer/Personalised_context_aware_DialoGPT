import json

import requests


def new_chat():
    endpoint = 'http://localhost:5000/new_chat/'
    request = requests.get(url=endpoint)
    return request.json()


def add_message_to_chat_history(sender, injected, message):
    endpoint = 'http://localhost:5000/add_message_to_history/'
    data = {
        "sender": sender,
        "injected": injected,
        "message": message
    }

    request = requests.post(url=endpoint, data=data)
    print("Post request status code = " + str(request.status_code))


def inject_bot_message(bot_message, user_message):
    endpoint = 'http://localhost:5000/inject_message/'
    data = {
        "bot_message": bot_message,
        "user_message": user_message
    }

    request = requests.post(url=endpoint, data=data)
    print("Post request status code = " + str(request.status_code))


# returns a tuple containing the near-to-realtime weather in the following format: [weather_info, weather_temperature]
def request_weather_information():
    endpoint = 'http://localhost:5000/request_weather/'
    request = requests.get(url=endpoint)
    json_object = json.loads(request.text)

    return [json_object["weather_type"], json_object["temperature"]]


def add_attribute_to_knowledge_base(key, value):
    endpoint = 'http://localhost:5000/add_knowledge_base/'
    data = {
        "key": key,
        "value": value
    }

    request = requests.post(url=endpoint, data=data)
    print("Post request status code = " + str(request.status_code))
