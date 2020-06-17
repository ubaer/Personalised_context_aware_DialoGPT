from gpt2bot.telegram_bot import main
#from gpt2bot.interactive_bot import main
from database.database_wrapper import check_and_prepare_mysql_database
from gpt2bot.context_determination import load_fasttext_model

check_and_prepare_mysql_database()
load_fasttext_model()

main()

#   van SQL naar Rest API gaan?
#   Context aan berichten hystory grote als parameter maken
#   Aantal berichten dat door het GTP2 model worden gegenereerd als parameter maken