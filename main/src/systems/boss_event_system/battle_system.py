import pymongo

from clan_event.battle_types.battle import Battle
from clan_event.lifeform_types.enemy_type import Enemy
from systems.database_system import DatabaseSystem


class BattleSystem(DatabaseSystem):
    def start_new_battle(self, enemy: Enemy):
        # self.event_battle_collection.delete_many({})
        battle = Battle(enemy=enemy)
        self.event_battle_collection.insert_one({
            'battle': battle.dict()
        })
        return battle

    def get_current_battle(self) -> Battle:
        battle_data = self.event_battle_collection.find_one({}, sort=[('_id', pymongo.DESCENDING)])
        return Battle.parse_obj(battle_data['battle'])

    def update_current_battle(self, battle: Battle):
        self.event_battle_collection.find_one_and_update({},
                                                         sort=[('_id', pymongo.DESCENDING)],
                                                         update={'$set': {'battle': battle.dict()}})
        return True


battle_system = BattleSystem()
