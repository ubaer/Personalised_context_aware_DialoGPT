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
Message injection is done through a mysql database. Any module that has access to this database can inject messages. However, it is HIGHLY recommended to inject everything through the rest_api.py API calls as it also handles all communication back to the user.<br>
The inject-message table has the following structure:<br>
| message_id 	| user_message          	| bot_message           	| injected         	|
|------------	|-----------------------	|-----------------------	|------------------	|
| int(auto)  	| text (default = NULL) 	| text (default = NULL) 	| int(default = 0) 	|

#### Context determination
##### Android
The android app can be used to extract information from a mobile phone and push it to the user profile. In this project the android app is not used anymore because it could not provide usefull enough information. However, the infrastructure still supports it for anyone that finds a use for it.
##### Text mining
Currently  [FastText](https://fasttext.cc/) is used to compare the context of sentences to determine the best response. It uses the [yahoo answers](https://fasttext.cc/docs/en/supervised-models.html) pre-trained model.
[spaCy](https://spacy.io/) is used to extract user information live during the conversation. In the current version only the name and origin country from the user is extracted. The user profile data is saved in the database table which is structured as follows:<br>
| id 	        | key_column          	    | value_column           	| 
|------------	|-----------------------	|-----------------------	|
| int(auto)  	| text (default = NULL) 	| text (default = NULL) 	| 
<br>
By using a key-value system the table structure, and thus the database structure, doesn't have to change when more modules are added or additional information is required. Any module can request information. If the requested key is not present, the requested information is unknown and the module can act accordingly.
<br>
During the project an opportunity arose to collaborate with another thesis project that also gathers user information during chat-bot conversations. 
In an effort to unify the way in which this type of data can be saved it is also possible to use a mongoDB database to save and retrieve this user data as long as it follows the following guidelines:
- The document present in the mongoDB database is in json format
- The document is uniquely identified by the telegram chat id of the specific user
- Modules should not give different meaning to keys that are already in use. Example: "name" is in this project used for the name of the interlocutor, another module should not change this value to anything other than the interlocutors name.
A mongoDB knowledge base entry example can be found [here](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/database/knowledge_base_entry_example.json)

##### Weather API
The weather API module is a great example of how external information can influence the chat bot.
The rule based bot is triggered by questions about weather which it can answer using real-time data provided by openweathermap. 
When the conversation continues and the rule based bot has no sufficient answers anymore the GTP2 bot will take over. It has knowledge about the previous messages send by the user and the rule-based bot. This includes the knowledge that is provided using the real-time weather API.
The weather API modules claims the knowledge base keys: "weather_type" and "weather_temp".
##### Rule based chat bot
To make the rule based bot as modular as possible a basic and simple approach has been chosen.
The bot is triggered by any word or phrase that is defined in the [synonyms.json](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/rulebased_bot/synonyms.json). 
Then the logic in [rulebased_bot.py](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/rulebased_bot/rulebased_bot.py) prepares the reply based on the category the user message belongs to.
This can be as simple as replying a random response from the identical category in [responses.json](https://github.com/ubaer/Personalised_context_aware_DialoGPT/blob/master/rulebased_bot/responses.json) or more complex by first gathering the relevant information from the knowledge base and then construct an appropriate reply.
