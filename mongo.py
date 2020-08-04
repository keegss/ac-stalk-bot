import pymongo
import pprint
from datetime import date

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["villager-database"]
        self.villagers = self.db['villagers']

    def enter_user_price(self, user: str, price: int, am_or_pm: str, day: str):

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
            self.villagers.insert_one(user_entry)

        return self.update_user_data(user_entry, price, am_or_pm, day)

    def update_user_data(self, user_entry, price, am_or_pm, day) -> bool:
        if int(day) < 0 or int(day) > 6:
            return False

        if int(day) < user_entry['expected_day']:
            # reset users week data
            reset_user_entry = {
                'user': user_entry['user'],
                'expected_day': user_entry['expected_day'],
                '0': [0, 0],
                '1': [0, 0],
                '2': [0, 0],
                '3': [0, 0],
                '4': [0, 0],
                '5': [0, 0]
            }
            self.villagers.delete_one({'user': 'keegs#7270'})
            self.villagers.insert_one(reset_user_entry)

        if am_or_pm == 'am':
            user_entry[day][0] = price
        else:
            user_entry[day][1] = price

        query = {'user': user_entry['user']}
        new_val = {'$set': {day: user_entry[day]}}        
        self.villagers.update_one(query, new_val)

        return True

    def predict(self):
        pass
        # is user
            # retrieve user from db
            # format string
            # API get to turnip calulator
        # else
            # User has no data associated!

    def close(self):
        self.client.close()

def main():
    mongo = Mongo()
    mongo.enter_user_price('keegs#7270', 165, 'am', '1')
    villagers = mongo.db.villagers
    pprint.pprint(villagers.find_one({'user': 'keegs#7270'}))
    pprint.pprint(villagers.find_one({'user': 'keegs#7270'}))
    mongo.close()

    # client = pymongo.MongoClient('mongodb://localhost:27017/')
    # db = client['mydatabase']
    # collection = db['test-collection']
    # print('um')
    # user1 = {
    #     'user': 'keegs#7270',
    #     '0': [0, 0],
    #     '1': [0, 0],
    #     '2': [0, 0],
    #     '3': [0, 0],
    #     '4': [0, 0],
    #     '5': [0, 0]
    #     }
    # user1 = {
    #     'user': 'potato#7271',
    #     '0': [0, 0],
    #     '1': [0, 0],
    #     '2': [0, 0],
    #     '3': [0, 0],
    #     '4': [0, 0],
    #     '5': [0, 0]
    #     }

    # print('test')
    # posts = db.posts
    # print('yo')
    # post_id = posts.insert_one(user1).inserted_id
    # print(post_id)

    # pprint.pprint(posts.find_one({'user': 'keegs#7270'}))

    # query = {'user': 'keegs#7270'}
    # new_value = {'$set': {'1': [160, 0]}} 
    # posts.update_one(query, new_value)

    # pprint.pprint(posts.find_one({'user': 'keegs#7270'}))

    # client.close()

if __name__ == '__main__':
    main()