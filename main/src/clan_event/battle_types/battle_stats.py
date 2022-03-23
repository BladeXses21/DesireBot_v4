from pydantic import BaseModel
from clan_event.lifeform_types.enemy_type import Enemy


class BattleStat(BaseModel):
    hero_id: int
    dmg_dealt: int = 0