from clan_event.life_form import LifeForm


class User(LifeForm):
    def __init__(self, name: str, health: int, user_id: int, atack_dmg: int):
        super().__init__(name, health)
        self.user_id = user_id
        self.atack_dmg = atack_dmg

