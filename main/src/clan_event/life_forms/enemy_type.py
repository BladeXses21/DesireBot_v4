from clan_event.life_forms.life_form import LifeForm


class Enemy(LifeForm):
    def __init__(self, name: str, health: int, attack_dmg: int, image: str):
        super().__init__(name, health)
        self.image = image
        self.attack_dmg = attack_dmg
