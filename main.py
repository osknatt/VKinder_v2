import random

from api.db import DB
from api.user import User
from constants import *

def main(lonely_user, context):
    '''
    Algorithm

    Criterion weights:
    (1) Common friends - 10 points for each friend
    (2) Common groups - 7 points for each group
    (3) Same city - 7 points
    (4) Same age - 8 points, and -1 for every year of difference.
    (5) Same interests - 5 points for each match.
    '''

    # Searching according to criteria
    print("Digging...")
    search_result = lonely_user.search(context['fields'], 
                                    context['sex'], 
                                    context['age'][0], 
                                    context['age'][1])
    search_result = search_result['response']['items']
    random.shuffle(search_result)
    result = []
    
    print("Rating candidates...")
    for s in search_result[:30]:
        points = 0

        # Common friends
        f = lonely_user.common_friends(s['id'])
        points += k_friends * f

        # Common groups
        if 'groups' in lonely_user.user_info['response'][0] and 'groups' in s:
            points += len(set(lonely_user.user_info['response'][0]['groups']).union(set(s['groups']))) * k_groups

        # Same city
        if 'city' in lonely_user.user_info['response'][0]:
            if 'city' in s and s['city']['title'] == lonely_user.user_info['response'][0]['city']['title']:
                points += k_city

        # Same age
        try:
            diff_year = int(lonely_user.user_info['response'][0]['bdate'].split('.')[-1]) - int(s['bdate'].split('.')[-1]) # Разница в возрасте
            points += k_age - abs(diff_year)
        except KeyError:
            pass

        # Same interests
        for elem in ['interest', 'music', 'books']:
            if elem in lonely_user.user_info['response'][0] and elem in s:
                points += len(set(lonely_user.user_info['response'][0][elem]).union(set(s[elem]))) * k_interests
        
        result.append([points, s['id'], f"{s['first_name']} {s['last_name']}", f"https://vk.com/id{s['id']}"])
        
    # Sorting results and saving
    result = sorted(result, key=lambda x:x[0], reverse=True)[:10]
    result_dict = {}
    for r in result:
        result_dict[r[1]] = r[2:]

    ctime = db_api.save(result_dict)

    # print(f'The recommendations were successfully recorded to results/{context["user_id"]}/{ctime}.json. You are welcome to donate :) ')
    print(f'The recommendations were successfully recorded to database result.db. You are welcome to donate :) ')

def check_age(age):
    if not '-' in age:
        raise ValueError('Invalid format. Try again.')
    age = list(map(int, age.split('-')))
    if age[0] > age[1]:
        reversed(age)
    if age[0] < 18:
        age[0] = 18
        print("We won't search among kids. Let's start from 18")
    if age[1] > 120:
        age[1] = 120
        print("We don't judge you, but we can't find such old people. Let's put 120 y.o. as maximum, that will be enough for you.")
    return age

def collect_input_data():
    user_id = input('Enter your ID for search: ')

    age = input('Enter age range in format xx-yy: ')
    age = check_age(age)
    sexis = {'b': 2,
             'g': 1,
             'd': 0}
    sex = input("Are you searching for boys / girls / doesn't matter [b/g/d]?: ")
    if not sex in ['b', 'g', 'd']:
        raise ValueError('Invalid format. Try again')

    context = {
        'user_id': user_id,
        'age': age,
        'sex': sexis[sex],
        'fields': 'sex, bdate, city, career, universities, schools, common_count, personal' \
                  'connections, activities, interests, music, movies, tv, books, games, about, photo_max',
    }
    return context

if __name__ == "__main__":
    context = collect_input_data()
    lonely_user = User(context['user_id'], context['fields'])
    db_api = DB(context['user_id'])
    main(lonely_user, context)
