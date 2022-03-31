from pydantic import BaseModel


class DmgRecord(BaseModel):
    hero_id: int
    dmg_dealt: int = 0

    def record_dmg(self, dmg: int):
        self.dmg_dealt = self.dmg_dealt + dmg
