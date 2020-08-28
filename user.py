import config
from print_results import print_results, get_results
from datetime import datetime
import telebot
from problem import Problem

bot = telebot.TeleBot(config.TOKEN)

class User:
    def __init__(self, chat_id, username,
                 test_scores=None,
                 total_scores=None,
                 test_start_time=datetime.now(), problem=None):
        self.chat_id = chat_id
        self.username = username
        self.test_scores = test_scores if test_scores else []
        self.total_scores = total_scores if total_scores else [0 for i in range(12)]
        self.test_start_time = test_start_time
        self.problem = problem

    ### Update info about user when new answers added

    def check_test(self):
        while len(self.test_scores) < 12: ### this will happen if a user haven't filled in all the answers
            self.test_scores.append(0)  ### TODO no while
        self.total_scores = [self.total_scores[i] + self.test_scores[i] for i in range(12)]
        bot.send_message(self.chat_id, print_results(self.test_scores), parse_mode='html')

    def skip_question(self):
        self.test_scores.append(0)

    def add_answer(self, user_answer):
        # self.current_answers.append(user_answer)
        self.test_scores.append(int(user_answer == self.problem.answer)) ### TODO don't convert to int
        self.problem.problem_number += 1

    def start_test(self):
        self.test_scores = []
        self.test_start_time = datetime.now()

    def scores_to_str(self):
        string = ''
        for el in self.test_scores:
            string += str(el) + ' '
        return string.strip(' ')

    def total_to_str(self):
        string = ''
        for el in self.total_scores:
            string += str(el) + ' '
        return string.strip(' ')

    def print_user_info(self):
        print(self.chat_id,
        self.username,
        self.test_scores)

