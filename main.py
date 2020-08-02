from gpt2bot.telegram_bot import main
# from gpt2bot.interactive_bot import main
from database.database_wrapper import check_and_prepare_mysql_database
from gpt2bot.context_determination import load_fasttext_model
from gpt2bot.api_wrapper import new_chat
from rulebased_bot.rulebased_bot import prepare_corpus

check_and_prepare_mysql_database()
load_fasttext_model()
prepare_corpus()

# Make call to API for new conversation
new_chat()

main()

#   Context aan berichten history grote als parameter maken
#   Aantal berichten dat door het GTP2 model worden gegenereerd als parameter maken
