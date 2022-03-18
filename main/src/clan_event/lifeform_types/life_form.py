from pydantic import BaseModel


class LifeForm(BaseModel):
    name: str
    current_health: int
    max_health: int

    def take_dmg(self, dmg: int):
        self.current_health = self.current_health - dmg

    def full_regen(self):
        self.current_health = self.max_health
