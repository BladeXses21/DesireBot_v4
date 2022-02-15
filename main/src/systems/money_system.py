from config import START_MONEY
from systems.database_system import DatabaseSystem


class MoneySystem(DatabaseSystem):
    def add_all_clan_members_into_collection(self, member_id: int):
        item = {"member_id": member_id, "money": START_MONEY}
        if self.money_collection.find_one({'member_id': member_id}):
            pass
        else:
            self.money_collection.insert_one(item)
            print(item)
            return True


def check_member(self, member_id: int):
    if self.money_collection.find_one({'member_id': member_id}):
        return False

    self.member_join(member_id, START_MONEY)
    return True


def member_join(self, author_id: int, amount: int):
    self.money_collection.insert_one({'member_id': author_id, 'member_cash': amount})
    return True


def award(self, author_id: int, amount: int):
    self.money_collection.update_one({'member_id': author_id, 'member_cash': amount})
    return True


money_system = MoneySystem()
