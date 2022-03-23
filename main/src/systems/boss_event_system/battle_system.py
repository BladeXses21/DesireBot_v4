from clan_event.battle_types.battle import Battle
from clan_event.lifeform_types.enemy_type import Enemy
from systems.database_system import DatabaseSystem


class BattleSystem(DatabaseSystem):
    def start_battle(self, enemy: Enemy):
        self.event_battle_collection.delete_many({})
        self.event_battle_collection.insert_one({
            'battle': Battle(enemy=enemy).dict()
        })
        return True

    def get_current_battle(self) -> Battle:
        battle_data = self.event_battle_collection.find_one({})
        return Battle.parse_obj(battle_data['battle'])

    def record_dealt_dmg(self, battle: Battle):
        # self.event_battle_collection.update_one({},
        #                                         {'$set': {'enemy': {'current_health': battle.enemy.current_health},
        #                                                   'stats': battle.stats}})
        self.event_battle_collection.update_one({},
                                                {'$set': {'battle': battle.dict()}})
        return True


battle_system = BattleSystem()
