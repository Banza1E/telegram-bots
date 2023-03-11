from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from config import TOKEN
from function import *

dialog_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
        LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, get_last_name)],
        PATERNAME: [MessageHandler(Filters.text & ~Filters.command, get_patername)],
        AGE: [MessageHandler(Filters.text & ~Filters.command, get_age)]
    },
    fallbacks=[CommandHandler('end', end)]
)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(dialog_handler)

print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C
