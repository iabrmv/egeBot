import sqlite3
from user import User
from print_results import string_to_int
import config
import random
from problem import Problem

#SQLighter(database_name).cursor.execute('DROP TABLE users')
class SQLighter:

    #### Connecting to DB

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()


    #### Creates an instance of user with selected chat_id

    def select_by_chat_id(self, chat_id):
        with self.connection:
            id, username, test_scores, total_scores = \
                self.cursor.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,)).fetchall()[0]

            return User(chat_id=chat_id, username=username,
                        test_scores=string_to_int(test_scores),
                        total_scores=string_to_int(total_scores))
    #### Add a user to a database

    def add_user(self, user): ###user should be an instance of User class
        with self.connection:
            self.cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)", (user.chat_id,
                                                                user.username,
                                                                user.scores_to_str(),
                                                                user.total_to_str()
                                                                ))

    def get_users(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users').fetchall()

    def get_problems(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM problems').fetchall()

    # Updates info in the database with the new user info

    def update_user(self, user):
        with self.connection:
            self.cursor.execute("""UPDATE users
            SET username = :username, 
                test_scores = :test_scores,
                total_scores = :total_scores 
            WHERE chat_id=:chat_id""", {
                                        'chat_id': user.chat_id,
                                        'username': user.username,
                                        'test_scores': user.scores_to_str(),
                                        'total_scores': user.total_to_str()
                                        })

    def add_problem(self, file_id, problem_id, problem_number, answer, level):
        with self.connection:
            self.cursor.execute("INSERT OR REPLACE INTO problems VALUES (?, ?, ?, ?, ?)", (file_id,
                                                                                        problem_id,
                                                                                        problem_number,
                                                                                        answer,
                                                                                        level
                                                                                        ))
    def delete_problem_by_id(self, problem_id):
        with self.connection:
            self.cursor.execute('''DELETE FROM problems
        WHERE problem_id = ?''', (problem_id,))

    def delete_problem_by_number(self, problem_number):
        with self.connection:
            self.cursor.execute('''DELETE FROM problems
        WHERE problem_id = ?''', (problem_number,))

    def select_random_problem_by_problem_number(self, problem_number=1):
        with self.connection:
            problems = self.cursor.execute('''SELECT * FROM problems
        WHERE problem_number = ?''', (problem_number,)).fetchall()
            random_problem_data = random.choice(problems) ### TODO random.choice
            problem = Problem(*random_problem_data)
            return problem

    def select_problem_by_id(self, file_id):
        with self.connection:
            problem_data = self.cursor.execute('''SELECT * FROM problems
               WHERE file_id = ?''', (file_id,)).fetchall()[0]
            problem = Problem(*problem_data)
            return problem

    def add_users_table(self):
        with self.connection:
            DB.cursor.execute('''CREATE TABLE users (
            chat_id INT PRIMARY KEY,
            username TEXT,
            test_scores TEXT,
            total_scores TEXT);''')

    def remove_table(self, table_name):
        with self.connection:
            self.cursor.execute(f'DROP TABLE ' + table_name +';')
    def close(self):
        self.connection.close()

DB = SQLighter(config.database_name)
#
# DB.remove_table('users')
# DB.add_users_table()

data_base = DB.get_users()
print(data_base)
#
#
# user_info = [[user[0], user[2], user[3], user[9]] for user in data_base]
# for i in user_info:
#     print(i)
#


#
# problems_DB = SQLighter(config.database_name).get_problems()
# for i in problems_DB:
#     print(i)




# with DB.connection:
#     DB.cursor.execute('''CREATE TABLE problems (
#     file_id TEXT PRIMARY KEY,
#     problem_id INT,
#     problem_number INT,
#     answer TEXT,
#     level INT);
#      ''')

