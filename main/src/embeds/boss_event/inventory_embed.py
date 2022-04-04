from discord import Embed, Colour

from game_event.model.lifeform_types.hero_type import Hero


class HeroInventoryEmbed(object):
    def __init__(self, hero: Hero, selected: int):
        self.cursor = '<:arrow:959084748796465222>'
        self._embed = Embed(title=f'{hero.name} inventory: ', color=Colour(0x292b2f))
        inventory = hero.inventory
        equipped = inventory.equipped

        helmet = equipped.helmet.name if equipped.helmet is not None else "Empty"
        gloves = equipped.gloves.name if equipped.gloves is not None else "Empty"
        chest = equipped.chest.name if equipped.chest is not None else "Empty"
        pants = equipped.pants.name if equipped.pants is not None else "Empty"
        boots = equipped.boots.name if equipped.boots is not None else "Empty"
        weapon = equipped.weapon.name if equipped.weapon is not None else "Empty"

        items_string = f"helmet : {helmet}"
        items_string = f"{items_string}\ngloves : {gloves}"
        items_string = f"{items_string}\nchest : {chest}"
        items_string = f"{items_string}\npants : {pants}"
        items_string = f"{items_string}\nboots : {boots}\n"
        items_string = f"{items_string}\nweapon : {weapon}\n"

        i = 1
        for item in inventory.items:
            if i == selected:
                items_string = f'{items_string}\n{self.cursor} {i}.  {item}'
            else:
                items_string = f"{items_string}\n{i}.  {item}"
            i = i + 1
        self._embed.description = f"{items_string}"

    @property
    def embed(self):
        return self._embed
