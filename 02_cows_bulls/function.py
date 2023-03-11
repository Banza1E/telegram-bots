from telegram.ext import Updater, Filters, MessageHandler, CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import pymorphy2
from sticker import *

morph = pymorphy2.MorphAnalyzer()
GO = 'Вперед!'
NAME = 1
BEGIN = 2
LEVEL = 3
GAME = 4
EASY, MED, HARD = 'Простой', "Средний", "Сложный"
SKIP = 'Пропустить'
SURR = 'Сдаться'


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}"!'
    )
    update.message.reply_sticker(START_STICKER)
    update.message.reply_text(
        f'''
        Поиграем в Быки и Коровы? 
        Игра для двоих: один участник загадывает слово, причем заранее оговаривается, сколько в нем должно быть букв.
        Задача второго — отгадать это слово, называя другие четырех - или пятибуквенные слова.
        Если какие-то буквы названного слова есть в загаданном, они называются «коровами», 
        а если у них совпадает и место внутри слова, то это «быки».
        Чтобы начать, нажми на кнопку {GO}!
        ''', reply_markup=keyboard)
    return NAME


def get_name(update: Update, context: CallbackContext):
    mark_up = [[SKIP]]
    full_name = update.effective_chat.full_name
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    update.message.reply_sticker(ASD)
    update.message.reply_text(f'Можно вас называть {full_name}? Если нет, то введите свое имя. Иначе - нажмите {SKIP}',
                              reply_markup=keyboard)
    return BEGIN


def begin(update: Update, context: CallbackContext):
    name = update.message.text
    if name == SKIP:
        name = update.effective_chat.full_name
    context.user_data['имя'] = name
    mark_up = [[EASY, MED, HARD]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'{EASY} - 3 буквы, {MED} - 4 буквы, {HARD} - 5 букв.'
    )
    update.message.reply_sticker(QWE)
    update.message.reply_text(f'{name}, выбери уровень сложности: ', reply_markup=keyboard)
    return LEVEL


def level(update: Update, context: CallbackContext):
    level_storage = update.message.text
    name = context.user_data['имя']
    if level_storage == EASY:
        with open('easy.txt', encoding='utf-8') as file:
            words = file.read().split('\n')
    elif level_storage == MED:
        with open('med.txt', encoding='utf-8') as file:
            words = file.read().split('\n')
    elif level_storage == HARD:
        with open('hard.txt', encoding='utf-8') as file:
            words = file.read().split('\n')
    else:
        update.message.reply_text('Недоступен файл')
    word = random.choice(words)
    context.user_data['word'] = word
    update.message.reply_text(f'{name}, отгадайте мое слово. Количество букв в слове: {len(word)}')
    return GAME


def game(update: Update, context: CallbackContext):  # callback
    my_word = update.message.text
    tag = morph.parse(my_word)[0]
    secret_word = context.user_data['word']  # достаем из рюкзака
    mark_up = [[SURR]]
    if len(secret_word) != len(my_word) and not my_word.isalpha():
        update.message.reply_text("Неверный ввод данных!")
        return
    elif my_word != tag.normal_form or tag.tag.POS != 'NOUN' or 'DictionaryAnalyzer()' not in str(tag.methods_stack):
        update.message.reply_text(f'Нужно вводить НОРМАЛЬНЫЕ слова...')
        return
    cows = 0
    bulls = 0
    for mesto, letter in enumerate(my_word):
        if letter in secret_word:
            if my_word[mesto] == secret_word[mesto]:
                bulls += 1
            else:
                cows += 1
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        input_field_placeholder=f'Нажмите кнопку {SURR}, чтобы сдаться.'
    )
    update.message.reply_text(f'В вашем слове {cows} коров и {bulls} быков')

    if bulls == len(secret_word):
        update.message.reply_text('Вы угадали! Вы красавчик')
        del context.user_data['word']
        return end(update, context)


def end(update: Update, context: CallbackContext):
    name = context.user_data['имя']
    update.message.reply_text(f"Конец игры, {name}.")
    return ConversationHandler.END


def surr(update: Update, context: CallbackContext):
    asd = context.user_data['word']
    update.message.reply_text(f'К сожалению, вы не угадали слово. Слово: {asd}')
    return ConversationHandler.END
