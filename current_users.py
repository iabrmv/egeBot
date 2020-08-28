import config
from user import  User
from user_sqlite3 import SQLighter
import problem

### This class helps us to store information about users passing a test atm

DB = SQLighter(config.database_name)

class CurrentUsers:
    def __init__(self):
        self.users = {}

    def add_user(self, chat_id):
        self.users[chat_id] = DB.select_by_chat_id(chat_id)

    def delete_user(self, chat_id):
        DB.update_user(self.users[chat_id])        ### updating DB info about this user
        del self.users[chat_id]

    def testmode(self, chat_id): ### TODO naming
        #if self.users == {}:
        #    return False
        #else:
        return chat_id in self.users

    def print(self):
        if self.users != {}:
            for chat_id in self.users.keys():
                self.users[chat_id].print_user_info()

