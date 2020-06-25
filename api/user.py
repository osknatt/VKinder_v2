import requests
import json
from constants import version
with open("settings.json") as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

if not TOKEN:
    print("We coudn't find access token in settings. Go to README.md "
          "To avoid this warning please save your access token in settings.json")
    TOKEN = input('Enter token: ')
    with open("settings.json", 'w') as f:
        json.dump({'TOKEN': TOKEN}, f)




class User:
    def __init__(self, user_id, fields):
        self.user_id = user_id
        self.user_info = self.get_user_info(self.user_id, fields)

    def get_params(self, add_params):
        params = {
            'access_token': TOKEN,
            'v': version
        }
        if add_params:
            params.update(add_params)
        return params

    def get_request(self, method, params):
        url = f'https://api.vk.com/method/{method}'
        info = requests.get(url, params=params)
        info = info.json()
        if 'error' in info:
            raise ValueError(info['error']['error_msg'])
        return info

    def get_user_info(self, user_id, fields):
        add_params = {'user_ids' : user_id,
                  'fields': fields
                  }
        params = self.get_params(add_params)
        info = self.get_request('users.get', params)
        return info

    def search(self, fields, sex, age_from, age_to):
        add_params = {
                  'count': 1000,
                  'fields': fields,
                  'sex': sex,
                  'status': 1&6,
                  'age_from': age_from,
                  'age_to': age_to
                  }
        params = self.get_params(add_params)
        info = self.get_request('users.search', params)
        return info

    def common_friends (self, user_id):
        add_params = {'target_uid': user_id,
                  'source_uid': self.user_id
                      }
        params = self.get_params(add_params)
        try:
            info = self.get_request('friends.getMutual', params)
            common_friends = info['response']
        except ValueError:
            common_friends = []

        return len(common_friends)