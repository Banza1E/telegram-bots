from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
from function import *

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        BEGIN: [MessageHandler(Filters.text & ~Filters.command, begin)],
        GAME: [MessageHandler(Filters.text & ~Filters.command, game)]
    },
    fallbacks=[CommandHandler('end', end)]
)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

print('Сервер запущен')
dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()  # ctrl + c
