from telegram.ext import Updater, Filters, MessageHandler, CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import csv

GO = 'Поехали'
GAME = 1

def read_csv():
    with open('вопросы.csv', 'r', encoding='utf-8') as file:
        quest = list(csv.reader(file, delimiter='|'))
        return quest


def write_csv():
    with open('вопросы.csv', 'a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|', lineterminator='\n')
        worker.writerow(['Какая столица Татарстана?', 'Казань', "Астана", "Нурстултан", "Чечня"])


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}"!'
    )
    update.message.reply_text(
        f'''
        Добро пожаловать в викторину!
        ''', reply_markup=keyboard)
    return GAME


def game(update: Update, context: CallbackContext):



def end(update: Update, context: CallbackContext):
    name = context.user_data['имя']
    update.message.reply_text(f"Конец игры, {name}.")
    return ConversationHandler.END


