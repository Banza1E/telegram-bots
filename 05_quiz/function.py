from telegram.ext import Updater, Filters, MessageHandler, CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import csv
import time

GO = 'Поехали'
GAME = 1
QUESTIONS_ON_ROUND = 4

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
    questions = read_csv()
    random.shuffle(questions)
    questions = questions[:QUESTIONS_ON_ROUND]
    context.user_data['вопросы'] = questions
    context.user_data['right_answer'] = GO
    context.user_data['counter'] = 0
    return GAME


def game(update: Update, context: CallbackContext):
    questions = context.user_data['вопросы']

    user_answer = update.message.text
    right_answer = context.user_data['right_answer']
    if user_answer == GO:
        pass
    elif user_answer == right_answer:
        update.message.reply_text('Правильно!')
        context.user_data['counter'] += 1
    else:
        update.message.reply_text('Неправильно!')
    time.sleep(1)

    if len(questions) == 0:
        counter = context.user_data['counter']
        update.message.reply_text('Конец игры!')
        update.message.reply_text(f'Вы ответили правильно на {counter} вопроса!')
        return ConversationHandler.END
    answers = questions.pop() # выдергиваем из списка последний вопрос
    question_text = answers.pop(0) # выдергиваем из списка нулевой элемент
    right_answer = answers[0]
    context.user_data['right_answer'] = right_answer
    random.shuffle(answers)
    mark_up = [answers[:2], answers[2:]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_text(question_text, reply_markup=keyboard)


def end(update: Update, context: CallbackContext):
    name = context.user_data['имя']
    update.message.reply_text(f"Конец игры, {name}.")
    return ConversationHandler.END


