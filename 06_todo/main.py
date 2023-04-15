from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler,
    Filters,
    MessageHandler
)
from firework import *
from interupt import *
from start_menu import *
from config import TOKEN

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MENU: [MessageHandler(Filters.text & ~Filters.command, get_menu)],
        ACTION: [MessageHandler(Filters.text & ~Filters.command, wrong_message)]
    },
    fallbacks=[CommandHandler('end', cancel)]
)
dispatcher.add_handler(conv_handler)

print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C
