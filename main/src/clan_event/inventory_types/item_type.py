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


class Item(BaseModel):
    name: str
    type: EnumItemTypes = None

    def get_name(self):
        return self.name
