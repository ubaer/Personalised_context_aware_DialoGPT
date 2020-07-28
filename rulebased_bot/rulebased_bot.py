import random

import nltk
import json
from gpt2bot.api_wrapper import inject_bot_message
import re

# do something with remembering my name
base_words = ['hello', 'hey']
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


# todo dynamically load bindings from json file as well
def set_bindings():
    keywords['greet'] = []
    for word in list(syn_dict['hello']):
        keywords['greet'].append('.*\\b' + word + '\\b.*')

    for intent, keys in keywords.items():
        patterns[intent] = re.compile('|'.join(keys))


def load_responses():
    global responses
    with open(responses_file) as response_file:
        response_json = json.load(response_file)
        for response in response_json:
            response_list = []
            for sentence in response_json[response]:
                response_list.append(sentence)
            responses[response] = set(response_list)
    print(responses)


# Returns empty string when no intent if found, returns the appropriate message if intent is found
def check_message_intent(message):
    matched_intent = None
    reply_message = ""

    for intent, pattern in patterns.items():
        if re.search(pattern, message):
            matched_intent = intent

    if matched_intent is not None:
        # todo instead of random use history of send messages to pick one that isn't used yet
        reply_message = random.sample(responses[matched_intent], 1)
        inject_bot_message(reply_message)
    return reply_message
