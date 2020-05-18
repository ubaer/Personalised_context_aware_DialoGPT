# from gpt2bot.telegram_bot import main
from gpt2bot.interactive_bot import main
from database.database_wrapper import check_and_prepare_mysql_database

check_and_prepare_mysql_database()

main()

#  van SQL naar Rest API gaan?
