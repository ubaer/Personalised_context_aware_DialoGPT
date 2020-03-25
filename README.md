# Context aware personalised chat bot
CaPchat is based on the [gpt2bot](https://github.com/polakowo/gpt2bot) telegram DialoGPT bot.

## How to use
#### Dependencies 
Dependencies that are required to run the bot are in [requirements.txt](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/requirements.txt). Note that some virtual environments can't download torch 1.2.0, newer versions give unexpected results and should not be used! Torch 1.2.0 can be downloaded from the [official website](https://download.pytorch.org/whl/torch_stable.html) and should be installed manually through pip.
#### No telegram
The bot is usable without telegram by running the main of [interactive_bot.py](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/gpt2bot/interactive_bot.py) in the project main.
#### Telegram
To avoid leakage to API keys the secrets file of this project is not commited. Follow these steps to launch your Telegram bot:
- Register a new Telegram bot via BotFather (see https://core.telegram.org/bots)
- Create a file named ```secrets.cfg``` in the root folder of the. The structure of the file should be as followed:
    ```
  [chatbot]
    # Your Telegram token. See https://core.telegram.org/bots
    telegram_token = TOKEN
    
    # Your GIPHY API token. 
    giphy_token = TOKEN
    ```
 - Run the main of [telegram_bot.py](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/gpt2bot/telegram_bot.py) in the project main.
 
 ## Information about modules
  This section will be updated throughout the project.
 #### Message injection
 Currently messages can be injected through the SQLite database generated in the database folder. Run the project once for it to auto generate the database and its tables.
 Then messages can be injected by adding rows in the 'inject_message' table. Injected messages are always put in front of the next message the user sends.
 
