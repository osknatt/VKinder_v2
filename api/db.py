import datetime
import json
import os
import sqlite3

class DB:
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = sqlite3.connect("result.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lonely_users
                                  (id INTEGER PRIMARY KEY)
                               """)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS candidates
                                          (id INTEGER, 
                                          name_surname TEXT,
                                          link TEXT,
                                          lonely_users_id INTEGER,
                                          FOREIGN KEY (lonely_users_id) REFERENCES lonely_users (id))
                                       """)
        self.conn.commit()

    def save(self, lovers):
        self.cursor.execute("""INSERT INTO lonely_users
                    VALUES (?);
        """, (self.user_id,))
        self.conn.commit()

        for l in lovers:
            self.cursor.execute("""INSERT INTO candidates
                            VALUES (?, ?, ?, ?);
                """, (l, lovers[l][0], lovers[l][1], self.user_id))
        self.conn.commit()

        # if 'results' not in os.listdir('.'):
        #     os.mkdir('./results')
        #
        # if str(self.user_id) not in os.listdir('./results/'):
        #     os.mkdir(f"./results/{self.user_id}")
        #
        # ctime = datetime.datetime.now()
        # with open(f"./results/{self.user_id}/{ctime.strftime('%d %B %Y %H-%M-%S')}.json", "w") as f:
        #     json.dump(lovers, f, ensure_ascii=False, default=lambda o: '<not serializable>')
        # return ctime.strftime('%d %B %Y %H-%M-%S')



