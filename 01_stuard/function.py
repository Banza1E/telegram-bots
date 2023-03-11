import pymorphy2
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

morph = pymorphy2.MorphAnalyzer()

eat, drink = range(2)
chicken, fish, salad = 'курица', 'рыба', 'салат'
water, tea, coffee = 'вода', 'чай', 'кофе'


def start(update: Update):
    mark_up = [[chicken, fish, salad]]
    keyboard = ReplyKeyboardMarkup(
        mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    update.message.reply_text(
        f'''
        Приветствуем вас на борту! Что будете есть?
        ''', reply_markup=keyboard)
    return eat


def eat_action(update: Update, context: CallbackContext):
    mark_up = [[water, tea, coffee]]
    keyboard = ReplyKeyboardMarkup(
        mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    foodd = update.message.text
    context.user_data['food'] = foodd
    update.message.reply_text('Хорошо, что будете пить?', reply_markup=keyboard)
    return drink


def drink_action(update: Update, context: CallbackContext):
    mark_up = [[]]
    ReplyKeyboardMarkup(
        mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    drinkk = update.message.text
    fd = context.user_data['food']
    fd = morph.parse(fd)[0]
    context.user_data['drinkk'] = drinkk
    drinkk = morph.parse(drinkk)[0]
    fd = fd.inflect({'accs'}).word
    drinkk = drinkk.inflect({'accs'}).word
    update.message.reply_text(f'Вы заказали {fd} и {drinkk}. Ожидайте заказ в течение 10 минут.')
    return end


def end():
    return ConversationHandler.END
