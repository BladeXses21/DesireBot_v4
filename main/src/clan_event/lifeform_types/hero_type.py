from clan_event.inventory_types.hero_inventory import HeroInventory
from clan_event.lifeform_types.life_form import LifeForm


class Hero(LifeForm):
    def __init__(self, hero_id: int, name: str, current_health: int, max_health: int, attack_dmg: int,
                 inventory: HeroInventory):
        super().__init__(name, current_health, max_health)
        self.hero_id = hero_id
        self.attack_dmg = attack_dmg
        self.inventory = inventory
