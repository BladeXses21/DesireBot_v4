import time

from systems.database_system import DatabaseSystem


class EventsModeSystem(DatabaseSystem):

    def is_clan_events_mode(self, clan_control: int) -> bool:
        if self.clan_events_mode_collection.find_one({'clan_control_id': clan_control}):
            return True
        return False

    # Добавление нового ивентера в базу
    def add_new_clan_events_mode(self, control_role_id: int, member_id: int, add_time: int):

        if self.clan_events_mode_collection.find_one({'member_id': member_id}):
            return False

        self.clan_events_mode_collection.insert_one({
            'control_role_id': control_role_id,
            'member_id': member_id,
            'works_with_request_id': None,
            'member_check_work': False,
            'all_sum_events_end': 0,
            'sum_wasting_time': 0,
            'add_time': add_time
        })
        return True

    # достает works_with_request_id для дальнекйшей проверки/ 1 ивент предналежит 1 ивентеру
    def checks_event_mode_to_work(self, member_id: int):
        res = self.clan_events_mode_collection.find_one({'member_id': member_id})

        if res is None:
            return False

        return res['works_with_request_id']

    # Проверка на то, находится ли ивентер сейчас на ивенте или нет
    def find_clan_event_mode_is_working(self, member_id: int):

        res = self.clan_events_mode_collection.find_one({'member_id': member_id})

        if res is None:
            return False

        return res['member_check_work']

    # Удаление клан контрола с базы
    def remove_clan_events_mode(self, member_id: int):
        self.clan_events_mode_collection.delete_one({'member_id': member_id})
        return True

    # Находит клан контрола в базе, если его нет выдает ошибку
    def find_clan_events_mode_on_base(self, member_id: int):
        if self.clan_events_mode_collection.find_one({'member_id': member_id}):
            return member_id
        return False

    # Принятние запроса ивента ивентером
    def accept_request(self, message_id: int, member_id: int):
        self.clan_events_collection.update_one({'message_id': message_id}, {'$set': {'time_accept_request': int(time.time())}})
        self.clan_events_mode_collection.update_one({'member_id': member_id}, {'$set': {'works_with_request_id': message_id}})
        self.clan_events_mode_collection.update_one({'member_id': member_id}, {'$set': {'member_check_work': True}})
        return True

    # достает всех ивентеров с базы для таблицы
    def enumeration_events_mode(self, control_role_id: int):
        return self.clan_events_mode_collection.find({'control_role_id': control_role_id}, {'_id': 0,
                                                                                            'member_id': 1,
                                                                                            'all_sum_events_end': 1,
                                                                                            'sum_wasting_time': 1,
                                                                                            'add_time': 1}).sort('all_sum_events_end', -1)

    # Создание запроса ивента
    def request_create(self, message_id: int, clan_name: str, event_name: str, member_id: int):
        self.clan_events_collection.insert_one({
            'message_id': message_id,
            'clan_name': clan_name,
            'event_name': event_name,
            'member_id': member_id,
            'time_accept_request': None
        })
        return True

    # Получение данных об запросе ивента
    def get_request(self, message_id: int):
        res = self.clan_events_collection.find_one({"message_id": message_id})

        if res is None:
            return ()

        return res['clan_name'], res['event_name'], res['member_id']

    # Получение начала времени ивента
    def get_time_create_event(self, message_id: int):
        res = self.clan_events_collection.find_one({"message_id": message_id})

        if res is None:
            return ()

        return res['time_accept_request']

    # Отказ от ивента/окончание ивента - удаляет запрос
    def request_delete(self, message_id: int):
        self.clan_events_collection.delete_one({'message_id': message_id})
        return True

    # обнуляет поле works_with_request_id при окончание ивента и меняет поле работы на False
    def submit_request(self, member_id: int):
        self.clan_events_mode_collection.update_one({'member_id': member_id}, {'$set': {'works_with_request_id': None}})
        self.clan_events_mode_collection.update_one({'member_id': member_id}, {'$set': {'member_check_work': False}})
        return True

    # Добавление данных о проведенном ивенте в бд ивентера
    def adding_event_data_to_events_mode(self, member_id: int, waisting_time: int):
        self.clan_events_mode_collection.update_one({"member_id": member_id}, {'$inc': {'all_sum_events_end': 1}})
        self.clan_events_mode_collection.update_one({"member_id": member_id}, {'$inc': {'sum_wasting_time': waisting_time}})
        return True


events_system = EventsModeSystem()
