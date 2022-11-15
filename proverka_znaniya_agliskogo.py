
import random


def runer():
    """
    программа контролер
    :return: запускает функции в зависимости от ответа
    """
    choosing_an_action = input('Что вы хотите сделать?\n'
                               'Если добавить слока нажмите "1"\n'
                               'Если проверить знания нажмите "2"\n')
    if choosing_an_action == '1':
        function_of_adding_a_word('word.txt')
    elif choosing_an_action == '2':
        function_of_getting_a_name('word.txt')
    else:
        print(f'Неверный ввод\n{"-" * 14}')
        runer()


def function_of_adding_a_word(filename):
    """
    запись новых слов
    :param filename: путь к фаилу
    :return: перезапускает программу
    """
    word = input('Введите слово которое хотите добавить на Англиском:\n')

    translation_word = input('Введите его перевод на Русском:\n')

    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f'{word}: {translation_word}\n')
    runer()


def function_of_getting_a_name(filename):
    """
    получение имени пользователя и проверка его на правельность
    :param filename: путь к фаилу со словами для игры
    :return: имя пользователя и путь к фаилу со соловами
    """
    # получаем имя пользователя
    username = input('Привет, введите, пожалуйста, имя!'
                     '\nОно должно быть без пробелов, цифр и загравных букв.\n')
    # проверка имени пользователя на соответствия требованиям

    if username.count(' ') > 0:
        print('Кажется, в имени пользователя есть пробелы.')
        function_of_getting_a_name(filename)
    elif username.isalpha() is False:
        print('Кажется, в имени пользователя есть цифры.')
        function_of_getting_a_name(filename)
    elif username.islower() is False:
        print('Кажется, в имени пользователя есть заглавные буквы')
        function_of_getting_a_name(filename)
    else:
        print(f'Отлично, {username.title()}, давай начнем проверку знаний!')
        creating_a_dictionary(username, filename)


def creating_a_dictionary(username, filename):
    """
    создаём словарь слов
    :param username: имя пользователя
    :param filename: путь к фаилу со словами и переводами
    :return: имя пользователя, словарь вопросов и ответов, список ключей словаря
    """
    # создаём словарь слов
    dictionary_of_words = {}

    # создаём список ключей
    list_keys = []

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            key, item = line.split(': ')
            dictionary_of_words[key] = item.rstrip()
            list_keys.append(key)
    english_proficiency_test_function(username, dictionary_of_words, list_keys)


def english_proficiency_test_function(username, dictionary, list_keys):
    """
    функция проверки знаний английского
    :param username: имя пользователя
    :param dictionary: словарь со словами
    :return: имя пользователя и словарь результатов проверки
    :list_keys: список ключей
    """
    # словарь перемешанных ключей
    random_list_keys = random.sample(list_keys, len(list_keys))

    # словарь ответов и их правельности
    answers_dictionary = {}

    #

    for key in random_list_keys:
        print(f'{key}, {len(dictionary[key])}, начинается {dictionary[key][0]}***')
        answer = input()

        if answer == dictionary[key]:
            print(f'Верно. {key} — это {dictionary[key]}.')
        else:
            print(f'Неверно. {key.title()} — это {dictionary[key]}.')
        answers_dictionary[key] = answer == dictionary[key]

    game_statistics_output(username, answers_dictionary)


def game_statistics_output(username, answers_dictionary):
    """
    вывод статистики за игру
    :param username: имя пользователя
    :param answers_dictionary: словарь результатов игры
    :return: имя пользователя и результат игры в %
    """

    # словарь подведения ранга
    levels = {
        0: "Нулевой",
        1: "Так себе",
        2: "Можно лучше",
        3: "Норм",
        4: "Хорошо",
        5: "Отлично",
    }
    # переменная подсчёта количества вопросов
    answers_count = 0

    # количества правельных ответов
    count = 0
    print('Правильно отвечены слова:')
    # цикл подсчёта правельных ответов
    for i, key in enumerate(answers_dictionary.keys(), start=1):
        if answers_dictionary[key] is True:
            print(key)
            count += 1
        answers_count = i

    percentage_correct_answers = count / answers_count * 100

    print('______________________________')
    print('Неправильно отвечены слова:')
    # цикл подчсёта неправельных ответов
    for key in answers_dictionary.keys():
        if answers_dictionary[key] is False:
            print(key)
    # вывод ранга
    print(f'Ваш ранг: {levels[count]}')
    result_recording_function(username, percentage_correct_answers, 'history.txt')


def result_recording_function(username, percentage, filehistory):
    """
    записывает результат игры в отдельный фаил
    :param username: имя пользователя
    :param percentage: процент правельныз ответов
    :param filehistory: путь к фаилу куза записывает
    :return: путь к фаилу куда записывает
    """
    with open(filehistory, 'a', encoding='utf-8') as f:
        f.write(f'{username}: {percentage}\n')

    output_of_the_best_result(filehistory)


def output_of_the_best_result(filehistory):
    """
    функция вывода количества игр и
    3 лучших результатов
    :param filehistory: путь до фаила с результатими игр
    :return:
    """
    # переменная подсчёта сыграннных игр
    count = 0

    # словарь результатов
    dictionary_results = {}

    with open(filehistory, 'r', encoding='utf-8') as f:
        for line in f:
            name, percentage = line.split(': ')
            dictionary_results[name] = percentage.rstrip()
            count += 1

    # создаём словарь для сортировки
    sorted_dictionary_results = {}

    # заполняем список
    sorted_key = sorted(dictionary_results, key=dictionary_results.get)

    # переворачиваем список
    sorted_key.reverse()

    # цмкл заполнения отсортированного словоря
    for name in sorted_key:
        sorted_dictionary_results[name] = dictionary_results[name]
    print('-' * 25)
    print(f'Сыграно игр {count}')
    print(f'Список лучших результатов')

    # вывод 3 лучших результатов
    for i, (name, point) in enumerate(sorted_dictionary_results.items(), start=1):
        if i <= 3:
            print(f'{i} {name}: {point}%')
        else:
            break


runer()
