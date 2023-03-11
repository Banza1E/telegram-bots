import csv


def read_csv():
    with open('вопросы.csv', 'r', encoding='utf-8') as file:
        quest = list(csv.reader(file, delimiter='|'))
        print(quest)


def write_csv():
    with open('вопросы.csv', 'a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|', lineterminator='\n')
        worker.writerow(['Какая столица Татарстана?', 'Казань', "Астана", "Нурстултан", "Чечня"])




