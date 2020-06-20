#  Copyright (c) polakowo
#  Licensed under the MIT license.

import configparser
import argparse
import logging

from gpt2bot.api_wrapper import new_chat
from gpt2bot.model import download_model_folder, download_reverse_model_folder, load_model
from gpt2bot.decoder_wrapper import generateTurn

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def run_chat(model, tokenizer, config, mmi_model=None, mmi_tokenizer=None):
    turns = []
    # Parse parameters
    num_samples = config.getint('decoder', 'num_samples')
    max_turns_history = config.getint('decoder', 'max_turns_history')

    logger.info("Running the chatbot...")
    print("Bot >>>", "Just start texting me. If I'm getting annoying, type \"Bye\". To quit the chat type \"Quit\".")
    while True:
        prompt = input("User >>> ")
        if max_turns_history == 0:
            # If you still get different responses then set seed
            turns = []
        if prompt.lower() == 'bye':
            print("Bot >>>", "Bye")
            turns = []
            new_chat()
            continue
        if prompt.lower() == 'quit':
            break

        bot_message, turns = generateTurn(turns, prompt, max_turns_history, num_samples, model, tokenizer, config, None,
                                          None)

        print("Bot >>>", bot_message)


def main():
    # Script arguments can include path of the config
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', type=str, default="gpt2bot/chatbot.cfg")
    args = arg_parser.parse_args()

    # Read the config
    config = configparser.ConfigParser(allow_no_value=True)
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
        print("none used")
        mmi_model = None
        mmi_tokenizer = None

    # Run chatbot with GPT-2
    run_chat(model, tokenizer, config, mmi_model=mmi_model, mmi_tokenizer=mmi_tokenizer)


if __name__ == '__main__':
    main()
