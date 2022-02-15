from systems.database_system import DatabaseSystem


class ClanSystem(DatabaseSystem):
    def is_clan_leader(self, leader_id: int) -> bool:
        if self.clan_collection.find_one({'leader_id': leader_id}):
            return True
        return False

    def create_clan(self, leader_id: int, role_id: int, clan_name: str, voice_id: int, text_id: int, create_time: int):

        if self.clan_collection.find_one({'leader_id': leader_id}):
            return False

        self.clan_collection.insert_one({
            'leader_id': leader_id,
            'clan_role_id': role_id,
            'clan_name': clan_name,
            'voice_id': voice_id,
            'text_id': text_id,
            'all_online': 0,
            'zam_slot': 1,
            'start_member_slot': 25,
            'img_url': None,
            'create_time': create_time
        })

        self.clan_member_collection.insert_one({
            'clan_role_id': role_id,
            'member_id': leader_id,
        })

    def clan_invite(self, clan_role_id: int, member_id: int):
        new_clan_member = {"clan_role_id": clan_role_id, "member_id": member_id}
        self.clan_member_collection.insert_one(new_clan_member)
        return True

    def find_clan_member(self, member_id: int):
        if self.clan_member_collection.find_one({'member_id': member_id}):
            return member_id
        return False

    def delete_clan(self, leader_id: int) -> tuple:
        res = self.clan_collection.find_one({'leader_id': leader_id})

        if not res:
            return ()

        self.clan_collection.delete_one({'leader_id': leader_id})
        self.clan_member_collection.delete_many({'clan_role_id': res['clan_role_id']})
        return res['clan_role_id'], res['voice_id'], res['text_id']

    def get_clan_info(self, leader_id: int):
        return self.clan_collection.find_one({'leader_id': leader_id}, projection={'_id': False})


clan_system = ClanSystem()
