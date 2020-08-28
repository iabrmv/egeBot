import telebot
import config
from telebot import types
from correctness import check_answer_spelling
from user_sqlite3 import SQLighter
from user import User
from threading import Timer
from current_users import CurrentUsers

bot = telebot.TeleBot(config.TOKEN)
DB = SQLighter(config.database_name)
current = CurrentUsers() ### TODO перенести в package current_users

@bot.message_handler(commands=['start'])
def welcome(message):
    # initialize a new User instance
    user = User(chat_id=message.chat.id, username=message.from_user.username)
    # and add him/her to our database
    DB.add_user(user)
    # add a button
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Сдать тест")
    item2 = types.KeyboardButton("Помощь")
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЗдесь Вы сможете подготовиться к ЕГЭ по математике".format(
                         message.from_user),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main(message):
    chat_id = message.chat.id
    if message.from_user.is_bot:   ### защита от ботов
        bot.send_message(chat_id, 'You shall not pass')
    elif message.text == 'Сдать тест': ### сделать маппинг кнопок
        current.add_user(chat_id)
        current.users[chat_id].start_test()
        problem = DB.select_random_problem_by_problem_number()
        current.users[chat_id].problem = problem
        bot.send_photo(chat_id, photo=problem.file_id,
                       caption="Введите ответ к заданию 1:", parse_mode='html')
        # set timer to terminate test in 30 min
        Timer(config.test_time, current.users[chat_id].check_test).start()
    elif message.text == 'Помощь':
        bot.send_message(message.chat.id,
                         "Ответ должен быть целым числом или десятичной дробью. Дробная часть отделяется запятой. Например: -0,516",
                         parse_mode='html')
    elif current.testmode(chat_id): #### which means that this user is passing test atm
        current_user = current.users[chat_id] ###TODO shorten
        if check_answer_spelling(message.text): #### TODO validation if.... else....
            current.users[chat_id].add_answer(message.text) ### TODO move chat_id to parameters
            if current.users[chat_id].problem.problem_number <= 12: ### TODO new method: CurrentUsers.get_problem_number(chat_id)
                print(f'current problem: {current.users[chat_id].problem.problem_number}')
                problem = DB.select_random_problem_by_problem_number(current.users[chat_id].problem.problem_number)
                current.users[chat_id].problem = problem
                bot.send_photo(chat_id, photo=problem.file_id,
                               caption=f"Введите ответ к заданию {current.users[chat_id].problem.problem_number}:",
                                 parse_mode='html')
            else:
                current.users[chat_id].check_test()
                current.delete_user(chat_id)
               # bot.send_message(message.chat.id, print_results(user.last_test_scores), parse_mode='html')
        else:
            bot.send_message(chat_id,
                             "Ответ должен быть целым числом или десятичной дробью. Введите ответ к заданию " +
                             str(current.users[chat_id].problem.problem_number) + ' еще раз.', parse_mode='html')

    else:
        bot.send_message(chat_id, 'Что-то пошло не так')

    print(f'message text: {message.text}')
    current.print()

#### Deal with time


# RUN
bot.polling(none_stop=True)
