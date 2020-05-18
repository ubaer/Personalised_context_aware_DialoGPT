#from gpt2bot.telegram_bot import main
from gpt2bot.interactive_bot import main
from database.database_wrapper import check_and_prepare_sqlite_database

check_and_prepare_sqlite_database()

main()
