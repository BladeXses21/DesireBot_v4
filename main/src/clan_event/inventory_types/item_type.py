from enum import Enum, unique


@unique
class EnumItemTypes(Enum):
    # armor
    helmet = 'helmet'
    chest = 'chest'
    boots = 'boots'
    gloves = 'gloves'
    pants = 'pants'

    weapon = 'weapon'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Item:
    @staticmethod
    def empty(self: EnumItemTypes):
        return Item("empty", self)

    def __init__(self, name: str, item_type: EnumItemTypes):
        self.name = name
        self.type = item_type
