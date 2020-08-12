from datetime import date
from typing import List, Tuple

import pymongo
import pprint
import requests

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["villager-database"]
        self.villagers = self.db['villagers']

    def enter_user_price(self, user: str, price: int, am_or_pm: str, day=None):
        if day == None: day = date.today().weekday()

        # if user is not present, create and add to db
        user_entry = self.villagers.find_one({'user': user})
        if user_entry is None:
            user_entry = {
                'user': user,
                'expected_day': date.today().weekday(),
                '0': [0, 0],
                '1': [0, 0],
                '2': [0, 0],
                '3': [0, 0],
                '4': [0, 0],
                '5': [0, 0]
            }
            user_entry[str(day)][0 if am_or_pm == 'am' else 1] = price
            self.villagers.insert_one(user_entry)
        else:
            return self.update_user_data(user_entry, price, am_or_pm, day)

    def update_user_data(self, user_entry, price, am_or_pm, day) -> bool:
        if day < 0 or day > 6:
            return False

        # TODO: reassess expected day reset logic          

        # mongo docs must have strings as keys
        str_day = str(day)
        user_entry[str_day][0 if am_or_pm == 'am' else 1] = price

        query = {'user': user_entry['user']}
        new_val = {'$set': {str_day: user_entry[str_day]}}        
        self.villagers.update_one(query, new_val)

        return True

    def predict(self, user: str) -> Tuple[List[int], List[int]]:
        user_entry = self.villagers.find_one({'user': user})
        if user_entry:
            # format and perform get call
            req_str = 'https://api.ac-turnip.com/data/?f='
            temp = ''
            for i in range(0, 6):
                temp = temp + '-' + str(user_entry[str(i)][0]) + '-' + str(user_entry[str(i)][1])
            req_str += temp           
            r = requests.get(req_str)

            res = r.json()
            min_max = res['minMaxPattern']
            avg_pattern = res['avgPattern']

            return (min_max, avg_pattern)
        else:
            # user has no data associated
            return None

    def reset_user(self, user: str):
        reset_user_entry = {
            'user': user_entry['user'],
            'expected_day': data.today.weekday(),
            '0': [0, 0],
            '1': [0, 0],
            '2': [0, 0],
            '3': [0, 0],
            '4': [0, 0],
            '5': [0, 0]
        }
        self.villagers.delete_one({'user': user_entry['user']})
        self.villagers.insert_one(reset_user_entry)

    def close(self):
        self.client.close()

def main():
    mongo = Mongo()
    villagers = mongo.db.villagers
    mongo.enter_user_price('keegs#7270', 185, 'am')
    min_max, avg = mongo.predict('keegs#7270')
    print(min_max)
    print(avg)
    mongo.close()

if __name__ == '__main__':
    main()