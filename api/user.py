import requests

from local import TOKEN, APP_ID

version = '5.107'


class User:
    def __init__(self, user_id, fields):
        self.user_id = user_id
        self.user_info = self.get_user_info(self.user_id, fields)

    def get_user_info(self, user_id, fields):
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': TOKEN,
                  'user_ids': user_id,
                  'fields': fields,
                  'v': version
                  }
        info = requests.get(url, params=params)
        info = info.json()
        return info

    def search(self, fields, sex, age_from, age_to):
        url = 'https://api.vk.com/method/users.search'
        params = {'access_token': TOKEN,
                  'count': 1000,
                  'fields': fields,
                  'sex': sex,
                  'status': 1&6,
                  'age_from': age_from,
                  'age_to': age_to,
                  'v': version
                  }
        data = requests.get(url, params=params)
        data = data.json()
        return data

    def common_friends (self, user_id):
        url = 'https://api.vk.com/method/friends.getMutual'
        params = {'access_token': TOKEN,
                  'target_uid': user_id,
                  'source_uid': self.user_id,
                  'v': version
                  }
        try:
            common_friends = requests.get(url, params=params)
            common_friends = common_friends.json()
            common_friends = common_friends['response']
        except:
            common_friends = []
        return len(common_friends)