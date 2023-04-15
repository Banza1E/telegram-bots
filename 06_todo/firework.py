from telegram import Update
from telegram.ext import CallbackContext
import csv
import os


def init(update: Update, context: CallbackContext):
    username = update.effective_user.username
    filename = f'database/{username}.csv'
    context.user_data['file'] = filename
    if not os.path.exists(f'database/{username}.csv'):
        os.mkdir('database')
        open(f'database/{username}.csv', 'w')


def read_csv():
    with open('вопросы.csv', 'r', encoding='utf-8') as file:
        quest = list(csv.reader(file, delimiter='|'))
        return quest


def write_csv():
    with open('вопросы.csv', 'a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|', lineterminator='\n')
        worker.writerow([])
