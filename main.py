from gpt2bot.telegram_bot import main
# from gpt2bot.interactive_bot import main
from database.database_wrapper import check_and_prepare_mysql_database, insert_chat_history_message, set_credentials
from gpt2bot.context_determination import load_fasttext_model
from gpt2bot.api_wrapper import new_chat

check_and_prepare_mysql_database()
load_fasttext_model()

# Make call to API for new conversation
new_chat()

main()

#   van SQL naar Rest API gaan?
#   Context aan berichten history grote als parameter maken
#   Aantal berichten dat door het GTP2 model worden gegenereerd als parameter maken
