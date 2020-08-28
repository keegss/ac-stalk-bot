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
        
        # TODO: create archive to save data for future ml study
        
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
            self.update_user_data(user_entry, price, am_or_pm, day)

        return self.formatted_user_data(user, user_entry)
    
    def formatted_user_data(self, user, user_entry=None):
        if user_entry is None:
            user_entry = self.villagers.find_one({'user': user})
        
        if user_entry is None:
            return None
        
        min_max, avg_pattern = self.predict(user, user_entry)

        week_data = ('"""\n```\n'
                     'Monday    : {}am {}pm\n'
                     'Tuesday   : {}am {}pm\n'
                     'Wednesday : {}am {}pm\n'
                     'Thursday  : {}am {}pm\n'
                     'Friday    : {}am {}pm\n'
                     'Saturday  : {}am {}pm\n'
                    #  'Min Max   : {}\n'
                     'Avg       : {}\n'
                     '```\n"""\n'
                    ).format(user_entry['0'][0], user_entry['0'][1],
                             user_entry['1'][0], user_entry['1'][1],
                             user_entry['2'][0], user_entry['2'][1],
                             user_entry['3'][0], user_entry['3'][1],
                             user_entry['4'][0], user_entry['4'][1],
                             user_entry['5'][0], user_entry['5'][1],
                             avg_pattern)
        return week_data

    def create_user_graph():
        # TODO: matplotlib dreams
        pass

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

    def predict(self, user, user_entry=None) -> Tuple[List[int], List[int]]:
        if user_entry is None:
            user_entry = self.villagers.find_one({'user': user})

        if user_entry is None:
            # user has no data associated
            return None

        # format and perform get call
        req_str = 'https://api.ac-turnip.com/data/?f='
        temp = ''
        for i in range(0, 6):
            temp = '{}-{}-{}'.format(temp, user_entry[str(i)][0], user_entry[str(i)][1])
        r = requests.get(req_str + temp)

        res = r.json()
        min_max = res['minMaxPattern']
        avg_pattern = res['avgPattern']

        return (min_max, avg_pattern)

    def reset_user(self, user: str):
        reset_user_entry = {
            'user': user,
            'expected_day': date.today().weekday(),
            '0': [0, 0],
            '1': [0, 0],
            '2': [0, 0],
            '3': [0, 0],
            '4': [0, 0],
            '5': [0, 0]
        }
        self.villagers.delete_one({'user': user})
        self.villagers.insert_one(reset_user_entry)

    def close(self):
        self.client.close()