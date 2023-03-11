from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
BEGIN, GAME = 1, 2
GO = 'Вперед'


def start(update: Update, _):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}"!'
    )
    update.message.reply_text(
        f'''
        Ты любишь придумывать сказки? 
        Я очень люблю. Ты знаешь сказку как посадил дед репку?
        А кто помогал деду репку тянуть? Чтобы начать, нажми на кнопку {GO}!
        ''', reply_markup=keyboard)
    return BEGIN


def begin(update: Update, context: CallbackContext):
    heroes = [['дедку'], ['дедка', 'репку']]
    context.user_data['heroes'] = heroes
    update.message.reply_text('''
                            Посадил дед репку. Выросла репка большая-пребольшая.
                            Стал дед репку из земли тянуть.
                            Тянет-потянет - вытянуть не может.
                            Кого позвал дедка?
                            ''', reply_markup=ReplyKeyboardRemove())
    return GAME


def game(update: Update, context: CallbackContext):
    message = morph.parse(update.message.text)[0]
    if message.tag.animacy == 'anim':
        nomn = message.inflect({'nomn'}).word
        accs = message.inflect({'accs'}).word
        heroes = context.user_data['heroes']
        heroes[0].insert(0, nomn)
        heroes.insert(0, [accs])
        answer = f'Я {nomn}. Буду помогать. '
        for nom, acc in heroes[1:]:
            answer += f'{nom.title()} за  {acc.title().lower()}. '
        if 'мыш' in nomn:
            update.message.reply_text(answer)
            update.message.reply_text('Тянули-тянули и вытянули репку!')
            return start(update, context)
        answer += 'Тянут-потянут - вытянуть не могут. '
        update.message.reply_text(answer)
        update.message.reply_text('Кого теперь позовем?')
    else:
        update.message.reply_text(f'Долго искали мы {message.normal_form}, ничего не нашли(')


def end(update: Update):
    update.message.reply_text('Конец')
    return ConversationHandler.END
