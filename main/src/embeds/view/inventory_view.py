from discord.ui import View

from embeds.view.buttons import buttons


class InventoryView(View):
    def __init__(self, back_callback, up_callback, down_callback, equip_callback, remove_callback):
        super().__init__(timeout=None)
        buttons.back_btn.callback = back_callback
        buttons.up_btn.callback = up_callback
        buttons.down_btn.callback = down_callback
        buttons.equip_btn.callback = equip_callback
        buttons.remove_item_btn.callback = remove_callback
        self.add_item(buttons.back_btn)
        self.add_item(buttons.up_btn)
        self.add_item(buttons.down_btn)
        self.add_item(buttons.equip_btn)
        self.add_item(buttons.remove_item_btn)