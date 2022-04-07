import time

from systems.database_system import DatabaseSystem
from config import CLANS


class ClanRatingSystem(DatabaseSystem):

    def add_clan_to_rating_system(self, clan_name: str, clan_text_id: int):
        if self.close_rating_collection.find_one({'clan_text_id': clan_text_id}):
            return False

        self.close_rating_collection.insert_one({
            'clan_name': clan_name,
            'clan_text_category': CLANS['CLAN_TEXT_CATEGORY'],
            'clan_text_id': clan_text_id,
            'clan_rating': 0,
            'clan_match': 0,
            'clan_sum_waiting_time': 0
        })
        return True

    def clan_victory_in_the_game(self, clan_text_id: int, clan_waisting_time: int):
        self.close_rating_collection.update_one({'clan_text_id': clan_text_id}, {'$inc': {'clan_rating': 25}})
        self.close_rating_collection.update_one({'clan_text_id': clan_text_id}, {'$inc': {'clan_match': 1}})
        self.close_rating_collection.update_one({'clan_text_id': clan_text_id}, {'$inc': {'clan_sum_waiting_time': clan_waisting_time}})
        return True

    def clan_loss_in_the_game(self, clan_text_id: int, clan_waisting_time: int):
        self.close_rating_collection.update_one({'clan_text_id': clan_text_id}, {'$inc': {'clan_rating': -25}})
        self.close_rating_collection.update_one({'clan_text_id': clan_text_id}, {'$inc': {'clan_match': 1}})
        self.close_rating_collection.update_one({'clan_text_id': clan_text_id}, {'$inc': {'clan_sum_waiting_time': clan_waisting_time}})
        return True

    def get_clan_rating_with_text_ids(self, clan_name: str):
        res = self.close_rating_collection.find_one({'clan_name': clan_name})
        return res['clan_text_id'], res['clan_rating'], res['clan_match'], res['clan_sum_waiting_time']

    def get_all_clan_rating_on_collection(self, clan_text_category: int):
        return self.close_rating_collection.find({'clan_text_category': clan_text_category}, {'clan_text_id': 1, 'clan_rating': 1}).sort('clan_rating', -1)

    def remove_from_rating(self, clan_name: str):
        self.close_rating_collection.delete_one({'clan_name': clan_name})
        return True


clan_rating_system = ClanRatingSystem()
