from clan_event.model.inventory_types.enemy_inventory import EnemyInventory
from clan_event.model.lifeform_types.life_form import LifeForm


class Enemy(LifeForm):
    image: str
    attack_dmg: int
    inventory: EnemyInventory = EnemyInventory()

    def take_dmg(self, dmg: int):
        super().take_dmg(dmg)

        if self.current_health <= 0:
            self.current_health = 0
