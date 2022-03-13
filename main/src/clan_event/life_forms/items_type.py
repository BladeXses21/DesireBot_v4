from enum import Enum, unique


@unique
class EnumItemTypes(Enum):
    hands = 'hands'
    helmet = 'helmet'
    spear = 'spear'
    onion = "onion"
    sword = 'sword'


class Item:
    def __init__(self, name: str, item_type: EnumItemTypes):
        self.name = name
        self.item_type = item_type
