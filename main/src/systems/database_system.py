from pymongo import MongoClient
from config import MongoToken


class DatabaseSystem(object):
    def __init__(self):
        self.client = MongoClient(MongoToken)
        self._db = self.client.desirebot

    @property
    def db(self):
        return self._db

    @property
    def clan_collection(self):
        return self.db.clan_collection

    @property
    def clan_member_collection(self):
        return self.db.clansmembers

    @property
    def money_collection(self):
        return self.db.membermoney
