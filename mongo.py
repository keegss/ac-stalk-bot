import pymongo

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.client["mydatabase"]

    def close():
        self.client.close()

if __name__ == "__main__":
    db = Mongo()