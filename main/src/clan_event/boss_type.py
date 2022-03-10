from clan_event.life_form import LifeForm


class Enemy(LifeForm):
    def __init__(self, name: str, health: int, atack_dmg: int, image: str):
        super().__init__(name, health)
        self.image = image
        self.atack_dmg = atack_dmg
