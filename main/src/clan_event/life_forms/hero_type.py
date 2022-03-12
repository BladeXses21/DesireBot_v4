from clan_event.life_forms.life_form import LifeForm


class Hero(LifeForm):
    def __init__(self, hero_id: int, name: str, health: int, attack_dmg: int):
        super().__init__(name, health)
        self.hero_id = hero_id
        self.attack_dmg = attack_dmg

