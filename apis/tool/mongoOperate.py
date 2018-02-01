from pymongo import MongoClient
import datetime
from django.conf import settings

class MongoOperate(object):
    def __init__(self, db_name):
        self.db_name = db_name

    def get_db(self):
        client = MongoClient(settings.SERVER_IP, 27017)
        db = client[self.db_name]
        return db

    def get_collection(self,col_name):
        db = self.get_db()
        coll = db[col_name]
        return coll

    def insert_records(self,coll, infomation):
        coll.insert(infomation)

    def get_one_doc(self,coll, kw):
        obje = coll.find_one(kw)
        return obje

    def get_many_docs(self,coll, kw = {}):
        docs = coll.find(kw)
        return docs

    def clear_collection(self,coll, condition={}):
        coll.remove(condition)

    #跟新collection保留一条有效数据
    def update_collection_withCondition(self, coll, newRecord,condition={}):
        #若存在MD5相同的文件 则删除其他，保留新的数据
        oldRecords = self.get_many_docs(coll, condition)
        if oldRecords:
            self.clear_collection(coll, condition)
        self.insert_records(coll, newRecord)
