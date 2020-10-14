# Context aware personalised chat bot
CaPchat is based on the [gpt2bot](https://github.com/polakowo/gpt2bot) telegram DialoGPT bot.
The android sensor collector module can be found [here](https://github.com/ubaer/CaPchat-Sensor-Information-Collector).
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
    active_chat_id = TELEGRAM_CHAT_ID_OF_CHAT
  
    # Your GIPHY API token. GIPHY is used to let the bot send GIFS, not tested nor maintained in this project. Might be broken, might be not
    giphy_token = TOKEN
  
    # Your mysql database information.
    db_username = USERNAME
    db_password = PASSWORD
    db_host = HOST_ADDRESS
    db_dbname = inject_message
  
    # External APIs
    openweathermap = API_KEY
    ```
 - Run the main of [telegram_bot.py](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/gpt2bot/telegram_bot.py) in the project main.
 
 ## Information about modules
  This section will be updated throughout the project.
 #### Message injection
Message injection is done through a mysql database. Any module that has access to this database can inject messages. The inject-message table has the following structure:<br>
| message_id 	| user_message          	| bot_message           	| injected         	|
|------------	|-----------------------	|-----------------------	|------------------	|
| int(auto)  	| text (default = NULL) 	| text (default = NULL) 	| int(default = 0) 	|

#### Context determination
##### Android
The android app can be used to extract information from a mobile phone and push it to the user profile. 
##### Text mining
Currently  [FastText](https://fasttext.cc/) is used to compare the context of sentences to determine the best response. It uses the [yahoo answers](https://fasttext.cc/docs/en/supervised-models.html) pre-trained model.
[spaCy](https://spacy.io/) is used to extract user information live during the conversation. In the current version only the name and origin country from the user is extracted. The user profile data is saved in the database table which is structured as follows:<br>
| id 	        | key_column          	    | value_column           	| 
|------------	|-----------------------	|-----------------------	|
| int(auto)  	| text (default = NULL) 	| text (default = NULL) 	| 
<br>
By using a key-value system the table structure, and thus the database structure, doesn't have to change when more modules are added or additional information is required. Any module can request information. If the requested key is not present, the requested information is unknown and the module can act accordingly.
##### Rule based chat bot
