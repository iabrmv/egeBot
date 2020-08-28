import re

def check_answer_spelling(answer):
    pattern = re.compile(r'0|(-?[1-9][0-9]*)|(-?[1-9][0-9]*,[0-9]*)|(-?0,[0-9]*)')
    if pattern.fullmatch(answer):
        return True
    else:
        return False

#def correct_spelling(answer):
#    return pattern.sub(r'\1\2\3\4', answer)