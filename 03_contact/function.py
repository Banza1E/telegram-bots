from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update

FIRST_NAME = 1
LAST_NAME = 2
PATERNAME = 3
AGE = 4


def start(update: Update):
    update.message.reply_text('Разговор начался. Давайте соберем данные о Вас.')
    update.message.reply_text('Назови мне свое имя или введи /end если хочешь прервать сбор данных.')
    return FIRST_NAME


def get_name(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data['name'] = name
    update.message.reply_text(f'Вы ввели имя {name}')
    update.message.reply_text(f'Назови мне свою фамилию или введи /end если хочешь прервать сбор данных.')
    return LAST_NAME


def get_last_name(update: Update, context: CallbackContext):
    last_name = update.message.text
    context.user_data['last_name'] = last_name
    update.message.reply_text(f'Вы ввели фамилию {last_name}')
    update.message.reply_text('Назови мне своё отчество или введи /end если хочешь прервать сбор данных.')
    return PATERNAME


def get_patername(update: Update, context: CallbackContext):
    patername = update.message.text
    context.user_data['patername'] = patername
    update.message.reply_text(f'Вы ввели отчество {patername}')
    update.message.reply_text('Назови мне свой возраст.')
    return AGE


def get_age(update: Update, context: CallbackContext):
    age = update.message.text
    if not age.isdigit():
        update.message.reply_text('Вы ввели не число!')
        return None
    age = int(age)
    if age > 90:
        update.message.reply_text('Вы ввели невалидный возраст.')
        return None
    context.user_data['age'] = age
    update.message.reply_text(f'Вы ввели возраст {age}')
    update.message.reply_text('Сбор данных завершен!')
    return ConversationHandler.END


def end(update: Update):
    update.message.reply_text("Сбор данных прерван")
    return ConversationHandler.END
