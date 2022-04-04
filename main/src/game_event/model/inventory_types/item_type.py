from enum import Enum, unique
import random

from pydantic import BaseModel, Field


@unique
class EnumItemTypes(str, Enum):
    helmet = 'helmet'
    chest = 'chest'
    boots = 'boots'
    gloves = 'gloves'
    pants = 'pants'
    weapon = 'weapon'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


# Todo item_rarity
@unique
class EnumItemRarity(str, Enum):
    mystery = 'Mystery'
    legendary = 'Legendary'
    epic = 'Epic'
    rare = 'Rare'
    common = "Common"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    def rarity_by(self, chance: int):
        randomRarity = random.choice(EnumItemRarity.list())

    def rarityIcon(self) -> str:
        if EnumItemRarity.common is self:
            return ":white_circle:"
        elif EnumItemRarity.rare is self:
            return ":blue_circle:"
        elif EnumItemRarity.epic is self:
            return ":purple_circle:"
        elif EnumItemRarity.legendary is self:
            return ":yellow_circle:"
        elif EnumItemRarity.mystery is self:
            return ":red_circle:"

    def rarity_chance(self):
        if EnumItemRarity.common is self:
            return 30
        elif EnumItemRarity.rare is self:
            return 60
        elif EnumItemRarity.epic is self:
            return 85
        elif EnumItemRarity.legendary is self:
            return 95
        elif EnumItemRarity.mystery is self:
            return 99


class Item(BaseModel):
    name: str
    type: EnumItemTypes
    rarity: EnumItemRarity = EnumItemRarity.common

    def get_name(self):
        return self.name

    def __str__(self):
        return f"{self.rarity.rarityIcon()} {self.name}"
