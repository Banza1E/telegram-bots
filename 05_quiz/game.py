from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler
)
from function import *
from config import TOKEN

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GAME: [MessageHandler(Filters.text & ~Filters.command, game)]
    },
    fallbacks=[CommandHandler('end', end)]
)
dispatcher.add_handler(conv_handler)

print('Приложение запущено')
updater.start_polling()
updater.idle()  # ctrl + C
