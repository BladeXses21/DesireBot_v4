from systems.database_system import DatabaseSystem
import time


class ControlSystem(DatabaseSystem):

    # def member_checks(self, member_id: int):
    #     self.clan_control_check_collection.insert_one({
    #         'member_id': member_id,
    #         'mon': None,
    #         'tue': None,
    #         'web': None,
    #         'thu': None,
    #         'fri': None,
    #         'sat': None,
    #         'sun': None,
    #         'all_ch': None
    #     })
    #     return True

    def is_clan_control(self, clan_control: int) -> bool:
        if self.clan_control_collection.find_one({'clan_control_id': clan_control}):
            return True
        return False

    def is_clan_curator(self, clan_curator_id: int) -> bool:
        if self.clan_curator_collection.find_one({'clan_curator_id': clan_curator_id}):
            return True
        return False

    def add_new_clan_control(self, control_role: int, member_id: int, add_time: int):

        if self.clan_control_collection.find_one({'member_id': member_id}):
            return False

        self.clan_control_collection.insert_one({
            'control_role': control_role,
            'member_id': member_id,
            'time_add': add_time,
            'check_num': 0,
            'time_check': None,
            'member_check_work': False,
            'time_kick': None
        })
        return True

    def add_new_clan_curator(self, member_id: int, add_time: int):
        if self.clan_curator_collection.find_one({'member_id': member_id}):
            return False

        self.clan_curator_collection.insert_one({
            'member_id': member_id,
            'time_add': add_time
        })

    def kick_clan_control(self, member_id: int):
        self.clan_control_collection.delete_one({'member_id': member_id})
        return True

    def find_clan_control_is_working(self, member_id: int):
        res = self.clan_control_collection.find_one({'member_id': member_id})

        if res is None:
            return ()

        return res['member_check_work'], res['time_check']

    def start_to_word(self, member_id: int, time_check: int):
        self.clan_control_collection.update_one({'member_id': member_id}, {'$set': {'member_check_work': True}})
        self.clan_control_collection.update_one({'member_id': member_id}, {'$set': {'time_check': time_check}})
        return True

    def return_to_work(self, member_id: int):
        self.clan_control_collection.update_one({'member_id': member_id}, {'$set': {'member_check_work': False}})
        self.clan_control_collection.update_one({'member_id': member_id}, {'$set': {'time_check': None}})
        self.clan_control_collection.update_one({'member_id': member_id}, {'$inc': {'check_num': 1}})
        return True

    def find_clan_control_on_base(self, member_id: int):
        if self.clan_control_collection.find_one({'member_id': member_id}):
            return member_id
        return False

    def enumeration_clan_control(self, clan_role: int):
        return self.clan_control_collection.find({'control_role': clan_role}, {'_id': 0, 'member_id': 1, 'check_num': 1, 'time_add': 1}).sort('check_num', -1)

    def clear_check(self, control_role_id: int):
        self.clan_control_collection.update_many({"control_role": control_role_id}, {'$set': {'check_num': 0}})
        return True


control_system = ControlSystem()
