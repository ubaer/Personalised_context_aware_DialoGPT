import copy
import pymongo
import datetime

""" The mongoDB_wrapper is an alternative to the knowledge base located in the relational database

mongoDB can be used instead of the 'key/value' table located in the relational database.
IT IS NOT A TOTAL REPLACEMENT FOR THE RELATIONAL DATABASE!
it still requires the relational database for message injection and chat history

To use this wrapper for external data injection just replace the imports used for get_weather_timestamp(),
get_weather_information() and insert_weather_information())to this file and call prepare_document() at main.py
"""

client = pymongo.MongoClient("mongodb://localhost:27017/")

mongo_db = client['thesis']
db = mongo_db['knowledgebase']

chat_id = ''


def prepare_document(telegram_chat_id):
    global chat_id
    chat_id = telegram_chat_id
    document = get_document_by_telegram_chat_id(telegram_chat_id)
    if document is None:
        new_document = {
            "telegram_chat_id": telegram_chat_id,
            "name": "",
            "weather_sensor": {
                "timestamp": "",
                "weather_temp": -0,
                "weather_type": ""
            }
        }
        db.insert_one(new_document)


def get_document_by_telegram_chat_id(telegram_chat_id):
    query = {"telegram_chat_id": telegram_chat_id}
    doc = db.find_one(query)
    return doc


def get_weather_timestamp():
    doc = get_document_by_telegram_chat_id(chat_id)
    timestamp = doc['weather_sensor']['timestamp']
    return timestamp


def get_weather_information():
    weather_info = [None, None]
    doc = get_document_by_telegram_chat_id(chat_id)
    weather_type = doc['weather_sensor']['weather_type']

    if weather_type != "":
        weather_temp = doc['weather_sensor']['weather_temp']
        weather_info = [weather_type, weather_temp]

    return weather_info


def insert_weather_information(weather_type, weather_temp):
    doc = get_document_by_telegram_chat_id(chat_id)
    old_doc = copy.deepcopy(doc)

    doc['weather_sensor']['timestamp'] = datetime.datetime.now()
    doc['weather_sensor']['weather_type'] = weather_type
    doc['weather_sensor']['weather_temp'] = weather_temp

    db.find_one_and_replace(old_doc, doc)
