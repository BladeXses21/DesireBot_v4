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
            'role_id': role_id,
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
            'leader_id': leader_id,
            'role_id': role_id,
            'clan_member': [
                {
                    'member_id': None,
                    'member_online': 0,
                    'invite_time': None
                }
            ]
        })

        self.clan_member_collection.update_one({
            'leader_id': leader_id
        },
            {'$set': {'clan_member': {'member_id': leader_id, 'invite_time': create_time}}}
        )
        return True

    def invite_clan(self, leader_id: int, member_id: int, invite_time: int):
        self.clan_member_collection.update_one({
            'leader_id': leader_id
        },
            {'$push': {'clan_member': {'member_id': member_id, 'invite_time': invite_time}}}
        )
        return True

    def delete_clan(self, leader_id: int) -> tuple:
        res = self.clan_collection.find_one({'leader_id': leader_id})

        if not res:
            return ()

        self.clan_collection.delete_one({'leader_id': leader_id})
        self.clan_member_collection.delete_one({'leader_id': leader_id})
        return res['role_id'], res['voice_id'], res['text_id']


clan_system = ClanSystem()
