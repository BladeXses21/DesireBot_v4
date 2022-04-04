from discord import ButtonStyle
from discord.ui import Button


class Buttons:
    def __init__(self):
        self.back_btn = Button(style=ButtonStyle.blurple, label='',
                               emoji='<:freeicon3dforwardarrow64844remov:960538574250471424>')
        self.attack_btn = Button(style=ButtonStyle.green, label='Attack',
                                 emoji="<:933511914707906590:960339513765429278>")
        self.profile_btn = Button(style=ButtonStyle.blurple, label='Profile',
                                  emoji="<:933511914384920577:960339396350050406>")
        self.inventory_btn = Button(style=ButtonStyle.blurple, label='Inventory',
                                    emoji='<:premiumiconbackpack4672563:960536938631270450>')
        self.up_btn = Button(style=ButtonStyle.gray,
                             emoji='<:up_arrow:960549187261460510> ')
        self.down_btn = Button(style=ButtonStyle.grey,
                               emoji='<:down_arrow:960549187194351706>')
        self.equip_btn = Button(style=ButtonStyle.green, emoji='<:icons896:960344174551502858>')

        self.choose_btn = Button(style=ButtonStyle.blurple, label='Choose')
        self.add_items_btn = Button(style=ButtonStyle.secondary, label='Add items')
        self.delete_btn = Button(style=ButtonStyle.red, label='Delete')

        self.detail_btn = Button(style=ButtonStyle.secondary, label='', emoji='ℹ')
        self.add_item_btn = Button(style=ButtonStyle.blurple, label='', emoji='➕')
        self.remove_item_btn = Button(style=ButtonStyle.red, label='', emoji='➖')

        self.enemies_btn = Button(style=ButtonStyle.secondary, label='Enemies')
        self.items_btn = Button(style=ButtonStyle.secondary, label='Items')
        self.heroes_btn = Button(style=ButtonStyle.secondary, label='Heroes')


buttons = Buttons()
