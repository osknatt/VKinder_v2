import unittest
from api.user import User
import json
from constants import version
from main import check_age

class AppTest(unittest.TestCase):
    def setUp(self):
        with open("settings.json") as f:
            data = json.load(f)
            self.TOKEN = data['TOKEN']
        self.user = User(user_id=0000, fields=[])

    def test_get_params(self):
        add_params = {'sex': 1}
        res = self.user.get_params(add_params)
        self.assertEqual(res, {
            'access_token': self.TOKEN,
            'v': version,
            'sex': 1
        })

    def test_check_age(self):
        age = '20-128'
        age = check_age(age)
        self.assertEqual(age, [20, 120])

if __name__ == '__main__':
    unittest.main()