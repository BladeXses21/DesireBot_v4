import time

from systems.database_system import DatabaseSystem


class ControlSystem(DatabaseSystem):

    def is_clan_control(self, clan_control: int) -> bool:
        if self.clan_control_collection.find_one({'clan_control_id': clan_control}):
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
            'time_kick': None,
            'check_queue': 0
        })
        return True

    def add_week_day_clan_control(self, member_id: int, control_role: int, member_name: str):
        self.clan_control_check_collection.insert_one({
            'control_role': control_role,
            'member_id': member_id,
            'member_name': member_name,
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            'all_day': 0
        })
        return True

    def kick_clan_control(self, member_id: int):
        self.clan_control_collection.delete_one({'member_id': member_id})
        self.clan_control_check_collection.delete_one({'member_id': member_id})
        return True

    def find_clan_control_is_working(self, member_id: int):

        res = self.clan_control_collection.find_one({'member_id': member_id})

        return res['member_check_work']

    def get_clan_control_check_num(self, member_id: int):
        res = self.clan_control_collection.find_one({'member_id': member_id})

        return res['check_num']

    def get_time_check(self, member_id: int):
        res = self.clan_control_collection.find_one({'member_id': member_id})

        return res['time_check']

    def start_to_word(self, member_id: int, time_check: int, today: int):
        self.clan_control_check_collection.update_one({'member_id': member_id}, {'$inc': {str(today): 1, "all_day": 1}})
        self.clan_control_collection.update_one({'member_id': member_id}, {'$inc': {'check_num': 1}})
        self.clan_control_collection.update_one({'member_id': member_id}, {'$set': {'member_check_work': True}})
        self.clan_control_collection.update_one({'member_id': member_id}, {'$set': {'time_check': time_check}})
        return True

    def check_queue(self, member_id):
        res = self.clan_control_collection.find_one({'member_id': member_id})

        return res['check_queue']

    def update_queue(self, member_id: int, control_role_id: int):
        check_queue = control_system.check_queue(member_id=member_id)
        if int(check_queue) == 0:
            self.clan_control_collection.update_many({"control_role": control_role_id}, {'$set': {'check_queue': 0}})
            self.clan_control_collection.update_one({'member_id': member_id}, {'$inc': {'check_queue': 1}})
            return True
        if int(check_queue) == 1:
            self.clan_control_collection.update_one({'member_id': member_id}, {'$inc': {'check_queue': 1}})
            return True

    def return_to_work(self, member_id: int):
        self.clan_control_collection.update_one({'member_id': member_id}, {'$set': {'member_check_work': False}})
        self.clan_control_collection.update_one({'member_id': member_id}, {'$set': {'time_check': None}})
        return True

    def find_clan_control_on_base(self, member_id: int):
        if self.clan_control_collection.find_one({'member_id': member_id}):
            return member_id
        return False

    def enumeration_clan_control(self, clan_role: int):
        return self.clan_control_collection.find({'control_role': clan_role}, {'_id': 0,
                                                                               'member_id': 1,
                                                                               'check_num': 1,
                                                                               'time_add': 1}).sort('check_num', -1)

    def clear_check(self, control_role_id: int):
        self.clan_control_collection.update_many({"control_role": control_role_id}, {'$set': {'check_num': 0}})
        self.clan_control_check_collection.update_many({"control_role": control_role_id}, {'$set': {'1': 0,
                                                                                                    '2': 0,
                                                                                                    '3': 0,
                                                                                                    '4': 0,
                                                                                                    '5': 0,
                                                                                                    '6': 0,
                                                                                                    '7': 0,
                                                                                                    'all_day': 0
                                                                                                    }})
        return True

    def time_start_checks_embed(self, start_check_time: int):
        self.clan_check_collection.insert_one({'server_name': 'Tenderly',
                                               'start_check_time': start_check_time
                                               })
        return True

    def remove_time_old_check(self, server_name: str):
        self.clan_check_collection.delete_one({'server_name': server_name})
        return True

    def check_validity(self, server_name: str):
        res = self.clan_check_collection.find_one({'server_name': server_name})

        return res['start_check_time']

    def view_checks_for_the_week(self, member_name: int):
        res = self.clan_control_check_collection.find_one({'member_name': member_name})
        return res['member_id'], res['1'], res['2'], res['3'], res['4'], res['5'], res['6'], res['7'], res['all_day']

    def find_all_clan_controllers_ids(self, control_role_id: int):
        return self.clan_control_check_collection.find({'control_role_id': control_role_id}, {'member_id': 1, 'all_day': 1}).sort('all_day', -1)


control_system = ControlSystem()
