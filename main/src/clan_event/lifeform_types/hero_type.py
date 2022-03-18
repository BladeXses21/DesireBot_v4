from clan_event.inventory_types.hero_inventory import HeroInventory
from clan_event.lifeform_types.life_form import LifeForm


class Hero(LifeForm):
    id: int
    attack_dmg: int
    inventory: HeroInventory = HeroInventory()

    def get_id(self):
        return self.id
