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
    
    # Your GIPHY API token. GIPHY is used to let the bot send GIFS, not tested nor maintained in this project. Might be broken, might be not
    giphy_token = TOKEN
  
    # Your mysql database information.
    db_username = USERNAME
    db_password = PASSWORD
    db_host = HOST_ADDRESS
    db_dbname = inject_message
    ```
 - Run the main of [telegram_bot.py](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/gpt2bot/telegram_bot.py) in the project main.
 
 ## Information about modules
  This section will be updated throughout the project.
 #### Message injection
Message injection is done through a mysql database. Any module that has access to this database can inject messages. The inject-message table has the following structure:<br>
| message_id 	| user_message          	| bot_message           	| injected         	|
|------------	|-----------------------	|-----------------------	|------------------	|
| int(auto)  	| text (default = NULL) 	| text (default = NULL) 	| int(default = 0) 	|

