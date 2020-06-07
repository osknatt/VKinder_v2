import json
import time
import random
import os
import datetime

from api.db import DB
from api.user import User

k_friends = 10
k_groups = 7
k_city = 7
k_age = 8
k_interests = 5

def main(lonely_user, context):
    '''
    Алгоритм вычисления совпадений

    Веса каждого критерия:
    (1) Общие друзья - 10 баллов за каждого друга
    (2) Общий группы - 7 баллов за каждую группу
    (3) Совпадение города - 7 баллов
    (4) Совпадение возраста - 8 баллов, если совпадение точное, -1 балл за каждый год расхождения
    (5) Совпадение интересов - 5 баллов за каждое совпадение.
    '''

    # Поиск по критериям
    print("Шурудим в VK")
    search_result = lonely_user.search(context['fields'], 
                                    context['sex'], 
                                    context['age'][0], 
                                    context['age'][1])
    search_result = search_result['response']['items']
    random.shuffle(search_result)
    result = []
    
    print("Оцениваем претендентов")
    for s in search_result[:30]:
        points = 0

        # Совпадение по общим группам
        f = lonely_user.common_friends(s['id'])
        points += k_friends * f

        # Совпадение по общим группам
        if 'groups' in lonely_user.user_info['response'][0] and 'groups' in s:
            points += len(set(lonely_user.user_info['response'][0]['groups']).union(set(s['groups']))) * k_groups

        # Совпадение по городу
        if 'city' in s and s['city']['title'] == lonely_user.user_info['response'][0]['city']['title']:
            points += k_city 

        # Совпадение по возрасту
        try:
            diff_year = int(lonely_user.user_info['response'][0]['bdate'].split('.')[-1]) - int(s['bdate'].split('.')[-1]) # Разница в возрасте
            points += k_age - abs(diff_year)
        except KeyError:
            pass

        # Совпадение по интересам
        for elem in ['interest', 'music', 'books']:
            if elem in lonely_user.user_info['response'][0] and elem in s:
                points += len(set(lonely_user.user_info['response'][0][elem]).union(set(s[elem]))) * k_interests
        
        result.append([points, s['id'], f"{s['first_name']} {s['last_name']}", f"https://vk.com/id{s['id']}"])
        
    # Сортировка результатов и сохранение в JSON
    print("Мы нашли подходящих личностей разных национальностей, сохраняем.")
    result = sorted(result, key=lambda x:x[0], reverse=True)[:10]
    result_dict = {}
    for r in result:
        result_dict[r[1]] = r[2:]

    db_api.save(result_dict)

    print('Рекомендации были созданы и записаны в файл! Донат приветствуется')

if __name__ == "__main__":
    # user_id = input('Введите Ваш ID для поиска подходящих партнеров: ')
    context = {
        'user_id': '957157',
        'age': [20,30],
        'sex': 2,
        'fields': 'sex, bdate, city, career, universities, schools, common_count, personal'\
        'connections, activities, interests, music, movies, tv, books, games, about, photo_max',
    }

    lonely_user = User(context['user_id'], context['fields'])
    db_api = DB(context['user_id'])
    main(lonely_user, context)

# Нужно сделать:
# вытащить 3 фото
# реализовать код для поиска не только по id но и по нику
