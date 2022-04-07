import time

from systems.database_system import DatabaseSystem


class CloseEventSystem(DatabaseSystem):

    def create_close_request(self, member_id: int, clan_send_request: str, clan_accept_request: str, message_request_id):
        if self.close_event_collection.find_one({'member_id': member_id}):
            return False

        self.close_event_collection.insert_one({
            'member_id': member_id,
            'member_id_accept_request': None,
            'message_request_id': message_request_id,
            'events_mode_id': None,
            'clan_send_request': clan_send_request,
            'clan_accept_request': clan_accept_request,
            'time_accept_request': None,
            'time_send_request': int(time.time())
        })
        return True

    # Принятние запроса ивента ивентером
    def accept_close_request(self, message_request_id: int, member_id_accept_request: int):
        self.close_event_collection.update_one({'message_request_id': message_request_id}, {'$set': {'member_id_accept_request': member_id_accept_request}})
        self.clan_events_mode_collection.update_one({'member_id': member_id_accept_request}, {'$set': {'works_with_request_id': message_request_id}})
        self.close_event_collection.update_one({'message_request_id': message_request_id}, {'$set': {'time_accept_request': int(time.time())}})
        self.clan_events_mode_collection.update_one({'member_id': member_id_accept_request}, {'$set': {'member_check_work': True}})
        return True

    def get_time_send_request(self, message_id: int):
        res = self.close_event_collection.find_one({'message_request_id': message_id})

        if res is None:
            return ()

        return res['time_send_request']

    def delete_close_request(self, message_request_id: int):
        self.close_event_collection.delete_one({'message_request_id': message_request_id})
        return True


close_event_system = CloseEventSystem()
