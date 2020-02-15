import pymongo
from pymongo.collection import Collection


class ConnectMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db_name = self.client['dou_guo']

    def insert_item(self, item):
        db_collection = Collection(self.db_name, 'dou_guo_item')
        db_collection.insert_one(item)

mongo_instance = ConnectMongo()
