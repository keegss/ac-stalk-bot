import pymongo
import pprint

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.client["villagers"]

    def enter_user_price(self, user, price, am_or_pm, day):

        # TODO:
            # when to clear the week??
            # force clear if next price is from day not expected?
                # day not expected = day < expected_day
                    # where day is user input
                    # expected day is last day entered

        # if no user
            # create all 0 for day and enter given day
        # if user
            # retrive user data from db and update day price

    def predict()

        # is user
            # retrieve user from db
            # format string
            # API get to turnip calulator
        # else
            # User has no data associated!

    def close():
        self.client.close()

def main():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    collection = db['test-collection']
    print('um')
    user1 = {
        'user': 'keegs#7270',
        '0': [0, 0],
        '1': [0, 0],
        '2': [0, 0],
        '3': [0, 0],
        '4': [0, 0],
        '5': [0, 0]
        }

    print('test')
    posts = db.posts
    print('yo')
    post_id = posts.insert_one(user1).inserted_id
    print(post_id)

    pprint.pprint(posts.find_one({'user': 'keegs#7270'}))

    client.close()

if __name__ == '__main__':
    main()