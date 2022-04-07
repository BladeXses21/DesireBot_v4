from discord import Embed, Colour

from game_event.model.lifeform_types.hero_type import Hero


class HeroInventoryEmbed(Embed):
    def __init__(self, hero: Hero, selected: int):
        super().__init__(title=f'{hero.name} inventory: ', color=Colour(0x292b2f))
        self.cursor = '<:arrow:959084748796465222>'
        inventory = hero.inventory
        equipped = inventory.equipped

        helmet = equipped.helmet.name if equipped.helmet is not None else " "
        gloves = equipped.gloves.name if equipped.gloves is not None else " "
        chest = equipped.chest.name if equipped.chest is not None else " "
        pants = equipped.pants.name if equipped.pants is not None else " "
        boots = equipped.boots.name if equipped.boots is not None else " "
        weapon = equipped.weapon.name if equipped.weapon is not None else " "

        items_string = f"<:helmet2:960570021036310568> : {helmet}"
        items_string = f"{items_string}\n<:gauntlet2:960570020960821349> : {gloves}"
        items_string = f"{items_string}\n<:chest2:960570021514453012> : {chest}"
        items_string = f"{items_string}\n<:pants2:960570027894001714> : {pants}"
        items_string = f"{items_string}\n<:boots:960570039721939034> : {boots}\n"
        items_string = f"{items_string}\nweapon : {weapon}\n"

        i = 1
        for item in inventory.items:
            if i == selected:
                items_string = f'{items_string}\n{self.cursor} {i}.  {item}'
            else:
                items_string = f"{items_string}\n{i}.  {item}"
            i = i + 1
        self.description = f"{items_string}"
