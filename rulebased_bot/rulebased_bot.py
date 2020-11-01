import random

import nltk
import json
from gpt2bot.api_wrapper import inject_bot_message, request_weather_information
from database.database_wrapper import get_user_profile_name
import re

# do something with remembering my name
keywords = {}
syn_dict = {}
patterns = {}
responses = {}

# Use this if you run this file separately
# synonyms_file = 'synonyms.json'
# responses_file = 'responses.json'
responses_file = 'rulebased_bot/responses.json'
synonyms_file = 'rulebased_bot/synonyms.json'


def prepare_corpus():
    nltk.download('wordnet')
    load_synonyms()
    set_bindings()
    load_responses()


def load_synonyms():
    with open(synonyms_file) as syn_file:
        syn_json = json.load(syn_file)
        for word in syn_json:
            synonyms = []
            for synonym in syn_json[word]:
                synonyms.append(synonym)
            syn_dict[word] = set(synonyms)


def set_bindings():
    with open(responses_file) as response_file:
        response_json = json.load(response_file)
        for category in response_json:
            keywords[category] = []
            for word in list(syn_dict[category]):
                keywords[category].append('.*\\b' + word + '\\b.*')

    for intent, keys in keywords.items():
        patterns[intent] = re.compile('|'.join(keys))


def load_responses():
    global responses
    with open(responses_file) as response_file:
        response_json = json.load(response_file)
        for response in response_json:
            response_list = []
            for sentence in response_json[response]:
                if isinstance(sentence, list):
                    sentence = tuple(sentence)
                response_list.append(sentence)
            responses[response] = set(response_list)


# Returns empty string when no intent if found, returns the appropriate message if intent is found
def check_message_intent(message):
    matched_intent = None
    reply_message = ""

    for intent, pattern in patterns.items():
        if re.search(pattern, message):
            matched_intent = intent

    print(matched_intent)

    if matched_intent is not None:
        if matched_intent == 'name_remember':
            name = get_user_profile_name()
            if name == '':
                reply_message = 'I don\'t know your name yet, what is it?'
            else:
                reply_message = str(random.sample(responses[matched_intent], 1)[0])
                reply_message += str(name)
        elif matched_intent == 'hello':
            # Check if the name of the user is known
            name = get_user_profile_name()
            if name is '':
                reply_message = str(random.sample(responses['request_name'], 1)[0])
            else:
                response = random.sample(responses[matched_intent], 1)[0]
                reply_message = str(response[0]) + name + str(response[1])
        elif matched_intent == 'weather_type':
            # using [0] as this is the weather_info
            current_weather_type = request_weather_information()[0]

            response = random.sample(responses[matched_intent], 1)[0]
            reply_message = str(response[0]) + current_weather_type + str(response[1])
        elif matched_intent == 'weather_temp':
            # using [1] as this is the weather_info
            current_weather_temp = request_weather_information()[1]

            response = random.sample(responses[matched_intent], 1)[0]
            reply_message = str(response) + str(current_weather_temp) + ' C'
        else:
            # todo instead of random use history of send messages to pick one that isn't used yet
            reply_message = str(random.sample(responses[matched_intent], 1)[0])

        print(reply_message)
        inject_bot_message(reply_message, message)
    return reply_message
