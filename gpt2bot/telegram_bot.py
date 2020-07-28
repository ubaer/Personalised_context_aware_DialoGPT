#  Copyright (c) polakowo
#  Licensed under the MIT license.

# !pip install python-telegram-bot --upgrade
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction, ParseMode
from functools import wraps
import configparser
import argparse
import logging
from urllib.parse import urlencode
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import re

from gpt2bot.model import download_model_folder, download_reverse_model_folder, load_model
from gpt2bot.decoder_wrapper import generateTurn
from gpt2bot.api_wrapper import new_chat, add_message_to_chat_history

# Rule based chat system
from rulebased_bot.rulebased_bot import check_message_intent

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets

def start_command(update, context):
    context.chat_data['turns'] = []
    update.message.reply_text(
        "Just start texting me. Append \"@gif\" for me to generate a GIF. If I'm getting annoying, type \"Bye\"")


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def translate_message_to_gif(message, config):
    # https://engineering.giphy.com/contextually-aware-search-giphy-gets-work-specific/
    params = {
        'api_key': config.get('chatbot', 'giphy_token'),
        's': message,
        'weirdness': config.getint('chatbot', 'giphy_weirdness')
    }
    url = "http://api.giphy.com/v1/gifs/translate?" + urlencode(params)
    response = requests_retry_session().get(url)
    return response.json()['data']['images']['fixed_height']['url']


def self_decorator(self, func):
    """Passes bot object to func command."""

    def command_func(update, context, *args, **kwargs):
        return func(self, update, context, *args, **kwargs)

    return command_func


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(self, update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(self, update, context, *args, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)


def gpt_normalize(txt):
    txt = re.sub(r"[^A-Za-z0-9()\[\]:,.!?'“”\"]", " ", txt)  # remove illegal chars
    return ' '.join(txt.strip().split())  # remove unnecessary spaces


@send_typing_action
def message(self, update, context):
    # Parse parameters
    num_samples = self.config.getint('decoder', 'num_samples')
    max_turns_history = self.config.getint('decoder', 'max_turns_history')
    if 'turns' not in context.chat_data:
        context.chat_data['turns'] = []
    turns = context.chat_data['turns']

    user_message = update.message.text
    add_message_to_chat_history('user', 0, user_message)

    if user_message.lower() == 'bye':
        # Restart chat
        context.chat_data['turns'] = []
        update.message.reply_text("Bye")
        add_message_to_chat_history('bot', 0, "Bye")
        new_chat()
        return None

    rule_based_response = check_message_intent(user_message.lower())

    # If
    if rule_based_response is "":
        if max_turns_history == 0:
            # If you still get different responses then set seed
            context.chat_data['turns'] = []

        bot_message, turns = generateTurn(turns, user_message, max_turns_history, num_samples, self.model,
                                          self.tokenizer,
                                          self.config, self.mmi_model,
                                          self.mmi_tokenizer)

        logger.info(f"{update.effective_message.chat_id} - Bot >>> {bot_message}")

        update.message.reply_text(bot_message)
        add_message_to_chat_history('bot', 0, bot_message)


def error(update, context):
    logger.warning(context.error)


class TelegramBot:
    def __init__(self, model, tokenizer, config, mmi_model=None, mmi_tokenizer=None):
        logger.info("Initializing the bot...")

        # Set global variables
        self.model = model
        self.tokenizer = tokenizer
        self.mmi_model = mmi_model
        self.mmi_tokenizer = mmi_tokenizer
        self.config = config

        # Set up Telegram bot
        self.updater = Updater(config.get('chatbot', 'telegram_token'), use_context=True)
        dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        # conversation with bot
        dp.add_handler(MessageHandler(Filters.text, self_decorator(self, message)))

        # chatbot settings
        dp.add_handler(CommandHandler('start', start_command))

        # log all errors
        dp.add_error_handler(error)

    def run_chat(self):
        logger.info("Running the chatbot...")

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()


def main():
    # Script arguments can include path of the config
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', type=str, default="gpt2bot/chatbot.cfg")
    args = arg_parser.parse_args()

    # Read the config
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("secrets.cfg")
    with open(args.config) as f:
        config.read_file(f)

    # Download and load main model
    target_folder_name = download_model_folder(config)
    model, tokenizer = load_model(target_folder_name, config)

    # Download and load reverse model
    use_mmi = config.getboolean('model', 'use_mmi')
    if use_mmi:
        mmi_target_folder_name = download_reverse_model_folder(config)
        mmi_model, mmi_tokenizer = load_model(mmi_target_folder_name, config)
    else:
        mmi_model = None
        mmi_tokenizer = None

    # Run Telegram bot
    bot = TelegramBot(model, tokenizer, config, mmi_model=mmi_model, mmi_tokenizer=mmi_tokenizer)
    bot.run_chat()


if __name__ == '__main__':
    main()
