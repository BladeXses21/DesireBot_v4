from pydantic import BaseModel
from clan_event.lifeform_types.enemy_type import Enemy


class DmgRecord(BaseModel):
    hero_id: int
    dmg_dealt: int = 0

    def record_dmg(self, dmg: int):
        self.dmg_dealt = self.dmg_dealt + dmg
