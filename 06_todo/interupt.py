from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    CallbackContext
)


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Спасибо за использование списка задач!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def wrong_message(update: Update, context: CallbackContext):
    update.message.reply_text('Упс! Такой команды не существует!')
