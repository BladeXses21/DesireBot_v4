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
        return self.db.clan_members

    @property
    def clan_member_details_collection(self):
        return self.db.clan_member_details

    @property
    def clan_zam_collection(self):
        return self.db.clan_zam

    @property
    def money_collection(self):
        return self.db.member_money

    @property
    def clan_control_collection(self):
        return self.db.clan_control

    @property
    def clan_curator_collection(self):
        return self.db.clan_curator

    @property
    def clan_control_check_collection(self):
        return self.db.clontrol_checks

    @property
    def event_boss_collection(self):
        return self.db.boss_collection

    @property
    def event_hero_collection(self):
        return self.db.hero_collection

    @property
    def event_battle_collection(self):
        return self.db.event_battle_collection

    @property
    def item_collection(self):
        return self.db.item_collection

