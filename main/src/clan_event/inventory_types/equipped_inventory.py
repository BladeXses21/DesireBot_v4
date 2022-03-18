from clan_event.inventory_types.item_type import Item, EnumItemTypes
from pydantic import BaseModel


class EquippedInventory(BaseModel):
    helmet: Item = None
    gloves: Item = None
    chest: Item = None
    pants: Item = None
    boots: Item = None

    def equip(self, item: Item):
        match item.type:
            case EnumItemTypes.helmet:
                self.helmet = item
            case EnumItemTypes.gloves:
                self.gloves = item
            case EnumItemTypes.chest:
                self.chest = item
            case EnumItemTypes.pants:
                self.pants = item
            case EnumItemTypes.boots:
                self.boots = item
            case _:
                print("That item cannot be equipped")
