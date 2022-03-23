from clan_event.inventory_types.enemy_inventory import EnemyInventory
from clan_event.lifeform_types.life_form import LifeForm


class Enemy(LifeForm):
    image: str
    attack_dmg: int
    inventory: EnemyInventory = EnemyInventory()

