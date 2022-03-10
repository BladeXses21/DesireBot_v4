class LifeForm:
    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health

    def take_dmg(self, dmg: int):
        self.health = int(self.health) - dmg
