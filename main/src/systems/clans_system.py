from systems.database_system import DatabaseSystem
import time
from config import CLANS


class ClanSystem(DatabaseSystem):
    def is_clan_leader(self, leader_id: int) -> bool:
        if self.clan_collection.find_one({'leader_id': leader_id}):
            return True
        return False

    def is_clan_user(self, member_id: int) -> bool:
        if self.clan_member_collection.find_one({'member_id': member_id}):
            return True
        return False

    def create_clan(self, leader_id: int, role_id: int, clan_name: str, voice_id: int, text_id: int, color,
                    create_time: int):

        if self.clan_collection.find_one({'leader_id': leader_id}):
            return False

        self.clan_collection.insert_one({
            'leader_id': leader_id,
            'clan_role_id': role_id,
            'clan_name': clan_name,
            'voice_id': voice_id,
            'text_id': text_id,
            'all_online': 0,
            'clan_member_slot': CLANS['CLAN_START_MEMBER_SLOT'],
            'zam_slot': 1,
            'clan_cash': 0,
            'img_url': None,
            'create_time': create_time,
            'clan_color': color,
            'deleted_at': None
        })

        self.clan_member_collection.insert_one({
            'clan_role_id': role_id,
            'member_id': leader_id,
            'deleted_at': None
        })

        self.clan_member_details_collection.insert_one({
            'clan_role_id': role_id,
            'member_id': leader_id,
            'member_online': 0,
            'member_invite_time': create_time,
            'member_afk': 0,
            'deleted_at': None
        })
        return True

    def clan_invite(self, clan_role_id: int, member_id: int, invite_time: int):
        new_clan_member = {"clan_role_id": clan_role_id, "member_id": member_id}
        member_details = {'clan_role_id': clan_role_id, "member_id": member_id, 'member_online': 0,
                          'member_invite_time': invite_time, 'member_afk': 0, 'delete_at': None}
        self.clan_collection.update_one({'clan_role_id': clan_role_id}, {'$set': {''}})
        self.clan_member_collection.insert_one(new_clan_member)
        self.clan_member_details_collection.insert_one(member_details)
        return True

    def find_clan_member(self, member_id: int):
        if self.clan_member_collection.find_one({'member_id': member_id}):
            return member_id
        return False

    def delete_clan(self, leader_id: int) -> tuple:
        res = self.clan_collection.find_one({'leader_id': leader_id})

        if not res:
            return ()

        # self.clan_collection.update_one({'leader_id': leader_id}, {'$set': {'deleted_at': int(time.time())}})
        # self.clan_member_collection.update_many({'clan_role_id': res['clan_role_id']},
        #                                         {'$set': {'deleted_at': int(time.time())}})
        # self.clan_member_details_collection.update_one({'clan_role_id': res['clan_role_id']},
        #                                                {'$set': {'deleted_at': int(time.time())}})
        self.clan_collection.delete_one({'leader_id': leader_id})
        self.clan_member_collection.delete_many({'clan_role_id': res['clan_role_id']})
        self.clan_member_details_collection.delete_many({'clan_role_id': res["clan_role_id"]})
        return res['clan_role_id'], res['voice_id'], res['text_id']

    def get_clan_info(self, leader_id: int):
        return self.clan_collection.find_one({'leader_id': leader_id}, projection={'_id': False})

    def get_clan_role_by_member_id(self, member_id: int):
        return self.clan_member_collection.find_one({'member_id': member_id}, projection={'_id': False})

    def get_clan_info_by_role_id(self, clan_role_id: int):
        return self.clan_collection.find_one({'clan_role_id': clan_role_id}, projection={'_id': False})

    def clan_profile(self, clan_role_id):
        return self.clan_member_details_collection.find({'clan_role_id': clan_role_id},
                                                        {'_id': 0, 'member_id': 1, 'member_online': 1}).sort(
            'member_online', -1)

    def set_flag(self, leader_id, image_url):
        self.clan_collection.update_one({'leader_id': leader_id}, {'$set': {'img_url': image_url}})
        return True


clan_system = ClanSystem()
