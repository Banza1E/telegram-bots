from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import TOKEN
from function import *

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        eat: [MessageHandler(Filters.text & ~Filters.command, eat_action)],
        drink: [MessageHandler(Filters.text & ~Filters.command, drink_action)]
    },
    fallbacks=[CommandHandler('end', end)]
)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

print('Сервер запущен')
dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()  # ctrl + F2
