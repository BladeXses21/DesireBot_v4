import time

from clan_event.model.inventory_types.hero_inventory import HeroInventory
from clan_event.model.lifeform_types.life_form import LifeForm
from config import HERO_RES_TIME


class Hero(LifeForm):
    id: int
    attack_dmg: int
    inventory: HeroInventory = HeroInventory()
    respawn_time: int = time.time()

    def get_dmg(self):
        return self.attack_dmg

    def take_dmg(self, dmg: int):
        super().take_dmg(dmg)

        if self.current_health <= 0:
            self.current_health = 0
            self.die()

    def die(self):
        self.respawn_time = int(time.time() + (3600 * HERO_RES_TIME))
        print(f"{self.respawn_time}")

    def is_dead(self):
        return self.respawn_time > time.time()

    def full_regen(self):
        self.current_health = self.max_health
        self.respawn_time = 0
