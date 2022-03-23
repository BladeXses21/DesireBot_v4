from enum import Enum, unique

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
class EnumItemRarity(int, Enum):
    legendary = 95
    epic = 80
    rare = 60
    gloves = 'gloves'
    pants = 'pants'
    weapon = 'weapon'

class Item(BaseModel):
    name: str
    type: EnumItemTypes = None

    def get_name(self):
        return self.name
