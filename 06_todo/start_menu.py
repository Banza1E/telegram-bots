from constants import *
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from firework import init
from stickers import start_sticker


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Для начала нажми на кнопку "{GO}"'
    )
    update.message.reply_sticker(start_sticker)
    update.message.reply_text(
        """Добро пожаловать в программу для учета списка ваших дел! Вы можете:
        - записывать дела
        - просматривать записанные
        - вносить в них изменения
        - удалять их
        - отмечать как выполненные        
        """
    )
    init(update, context)
    update.message.reply_text(
        f"Чтобы начать нажми на '{GO}'", reply_markup=keyboard
    )
    return MENU


def get_menu(update: Update, context: CallbackContext):
    mark_up = [[CREATE], [UPDATE, COMPLETE], [READ, DELETE]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_text(f'Выберите действие', reply_markup=keyboard)
    return ACTION