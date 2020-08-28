### Здесь будет функция, которая склоняет слово word в соответствии с числительным number
### decline(21, 'балл') _____ 21 балл
### decline(32, 'балл') ______ 32 балла
### decline(65, 'балл') ______ 65 баллов

def decline(number, word):
    if number in range(10, 20):
        return(str(number) + ' ' + word + 'ов')
    elif number % 10 == 1:
        return (str(number) + ' ' + str(word))
    elif number % 10 in [2, 3, 4]:
        return (str(number) + ' ' + str(word) + 'а')
    else:
        return (str(number) + ' ' + str(word) + 'ов')
