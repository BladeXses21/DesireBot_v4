from systems.database_system import DatabaseSystem
import time


class ControlSystem(DatabaseSystem):

    def is_clan_control(self, clan_control: int) -> bool:
        if self.clan_control_collection.find_one({'clan_control_id': clan_control}):
            return True
        return False

    def is_clan_curator(self, clan_curator_id: int) -> bool:
        if self.clan_curator_collection.find_one({'clan_curator_id': clan_curator_id}):
            return True
        return False

    def add_new_clan_control(self, member_id: int, add_time: int):

        if self.clan_control_collection.find_one({'member_id': member_id}):
            return False

        self.clan_control_collection.insert_one({
            'member_id': member_id,
            'time_add': add_time,
            'member_check': None,
            'time_kick': None
        })
        return True

    def add_new_clan_curator(self, member_id: int, add_time: int):
        if self.clan_curator_collection.find_one({'member_id': member_id}):
            return False

        self.clan_curator_collection.insert_one({
            member_id: member_id,
            'time_add': add_time
        })


control_system = ControlSystem()
