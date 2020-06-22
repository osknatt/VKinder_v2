import datetime
import json
import os


class DB:
    def __init__(self, user_id):
        self.user_id = user_id

    def save(self, lovers):
        if 'results' not in os.listdir('.'):
            os.mkdir('./results')

        if str(self.user_id) not in os.listdir('./results/'):
            os.mkdir(f"./results/{self.user_id}")

        ctime = datetime.datetime.now()
        with open(f"./results/{self.user_id}/{ctime.strftime('%d %B %Y %H-%M-%S')}.json", "w") as f:
            json.dump(lovers, f, ensure_ascii=False, default=lambda o: '<not serializable>')
        return ctime.strftime('%d %B %Y %H-%M-%S')

