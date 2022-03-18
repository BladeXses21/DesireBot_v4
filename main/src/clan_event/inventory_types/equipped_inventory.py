from clan_event.inventory_types.item_type import Item, EnumItemTypes


class EquippedInventory:
    def __init__(self, helmet: Item = None, gloves: Item = None, chest: Item = None, pants: Item = None,
                 boots: Item = None, weapon: Item = None):
        self.slots = {EnumItemTypes.helmet.value: helmet,
                      EnumItemTypes.gloves.value: gloves,
                      EnumItemTypes.chest.value: chest,
                      EnumItemTypes.pants.value: pants,
                      EnumItemTypes.boots.value: boots,
                      EnumItemTypes.weapon.value: weapon}


def equip(self, item: Item):
    self.slots.update({item.type: item})
