from pydantic import BaseModel

from clan_event.model.inventory_types.item_type import Item, EnumItemTypes


class EquippedInventory(BaseModel):
    helmet: Item = None
    gloves: Item = None
    chest: Item = None
    pants: Item = None
    boots: Item = None
    weapon: Item = None

    def equip(self, item: Item):
        previous_item: Item = None

        match item.type:
            case EnumItemTypes.helmet:
                previous_item = self.helmet
                self.helmet = item
            case EnumItemTypes.gloves:
                previous_item = self.gloves
                self.gloves = item
            case EnumItemTypes.chest:
                previous_item = self.chest
                self.chest = item
            case EnumItemTypes.pants:
                previous_item = self.pants
                self.pants = item
            case EnumItemTypes.boots:
                previous_item = self.boots
                self.boots = item
            case EnumItemTypes.weapon:
                previous_item = self.weapon
                self.weapon = item
            case _:
                print("That item cannot be equipped")
        return previous_item

    def unequip(self, item_type: EnumItemTypes):
        match item_type:
            case EnumItemTypes.helmet:
                self.helmet = None
            case EnumItemTypes.gloves:
                self.gloves = None
            case EnumItemTypes.chest:
                self.chest = None
            case EnumItemTypes.pants:
                self.pants = None
            case EnumItemTypes.boots:
                self.boots = None
            case EnumItemTypes.weapon:
                self.weapon = None
            case _:
                print("That item cannot be unequipped")
