import argparse
import configparser

import requests
import json
import datetime

from database.database_wrapper import get_weather_information, insert_user_profile, get_weather_timestamp

latitude = 52
longitude = 5.25
# How long weather info is valid until new data is requested from the API default = 10 as the openweathermap API only refreshes every ten minutes
weather_validity_in_minutes = 10


def request_weather_info():
    # check if 10 minutes since last update
    database_values = check_database()
    weather_type = database_values[0]
    temperature = database_values[1]

    if weather_type is None:
        # Read the config
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--config', type=str, default="gpt2bot/chatbot.cfg")
        args = arg_parser.parse_args()
        config = configparser.ConfigParser(allow_no_value=True)
        config.read("secrets.cfg")
        with open(args.config) as f:
            config.read_file(f)

        base_url = 'https://api.openweathermap.org/data/2.5/onecall?'
        lat_lon = 'lat={}&lon={}'.format(latitude, longitude)
        exclusions = '&exclude=minutely,hourly,daily'
        api_key = '&appid=' + config.get('chatbot', 'openweathermap')

        endpoint = base_url + lat_lon + exclusions + api_key
        request = requests.get(url=endpoint)
        print("Accessing Weather API")
        replaced = request.text.replace('\'', '"')
        json_object = json.loads(replaced)

        weather_type = str.lower(json_object["current"]["weather"][0]["description"])

        if weather_type == 'clear sky':
            weather_type = 'a clear sky'

        # -273.15 to convert Kelvin to Celsius
        temperature = round(json_object["current"]["temp"] - 273.15, 1)
        insert_weather_information(weather_type, temperature)

    return [weather_type, temperature]


def check_database():
    weather_info = [None, None]

    timestamp = get_weather_timestamp()
    current_time = datetime.datetime.now()

    minutes_added = datetime.timedelta(minutes=weather_validity_in_minutes)
    max_valid_datetime = timestamp + minutes_added

    if current_time < max_valid_datetime:
        weather_info = get_weather_information()

    return weather_info


def insert_weather_information(weather_type, weather_temp):
    insert_user_profile("weather_type", weather_type)
    insert_user_profile("weather_temp", weather_temp)
