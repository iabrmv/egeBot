import re
from decline import decline

def get_results(user_answers, true_answers): # returns the array of scores
    #### appending zeros to our array in out-of-time case
    if(len(user_answers) < len(true_answers)):
        print('ooops something went wrong')
    while len(user_answers) < len(true_answers):
        user_answers.append('NA')
    else:
        Length = len(user_answers)
        return [int(user_answers[i] == true_answers[i]) for i in range(Length)]

def str_for_DB(array):
    string = ''
    for el in array:
        string += str(el) + ' '
    return string.strip(' ')

def to_string(results):
    string = ''
    for i in range(12):
        if i < 9:
            string += str(i + 1) + ' ..... ' + str(results[i]) + '\n'
        else:
            string += str(i + 1) + ' .... ' + str(results[i]) + '\n'
    return string

def string_to_int(results):
    if results == '':
        return []
    else:
        results_array = results.split(' ')
        return [int(s) for s in results_array]

### makes a perfect string to be printed straight into telegram

def print_results(results):
    return "Вы сдали тест. Ваши баллы: \n\n" + "<code>" + to_string(results) + '</code>' + '\nИтого: ' + decline(sum(results), 'балл') + ' из 12'

