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
