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
    def clan_events_mode_collection(self):
        return self.db.clan_events_mode

    @property
    def clan_events_collection(self):
        return self.db.events_collection

    @property
    def clan_control_check_collection(self):
        return self.db.clontrol_checks

    @property
    def game_boss_collection(self):
        return self.db.boss_collection

    @property
    def game_hero_collection(self):
        return self.db.hero_collection

    @property
    def game_battle_collection(self):
        return self.db.battle_collection

    @property
    def item_collection(self):
        return self.db.item_collection

    @property
    def dmg_stats_collection(self):
        return self.db.dmg_stats_collection

    @property
    def close_event_collection(self):
        return self.db.close_event_collention

    @property
    def close_rating_collection(self):
        return self.db.clan_close_rating_system

    @property
    def clan_check_collection(self):
        return self.db.clan_check_collection
