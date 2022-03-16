from clan_event.lifeform_types.life_form import LifeForm


class Enemy(LifeForm):
    def __init__(self, name: str, current_health: int,  max_health: int, attack_dmg: int, image: str):
        super().__init__(name, current_health, max_health)
        self.image = image
        self.attack_dmg = attack_dmg
