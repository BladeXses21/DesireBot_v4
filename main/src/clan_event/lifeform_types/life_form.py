class LifeForm:
    def __init__(self, name: str, current_health: int, max_health: int):
        self.name = name
        self.current_health = current_health
        self.max_health = max_health

    def take_dmg(self, dmg: int):
        self.current_health = self.current_health - dmg

    def full_regen(self):
        self.current_health = self.max_health
