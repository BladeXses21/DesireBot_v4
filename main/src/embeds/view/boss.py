from discord.ui import View

from embeds.view.buttons import buttons


class BossView(View):
    def __init__(self, back_callback, add_items_callback, delete_callback):
        super().__init__(timeout= None)
        buttons.back_btn.callback = back_callback
        buttons.add_items_btn.callback = add_items_callback
        buttons.delete_btn.callback = delete_callback
        self.add_item(buttons.back_btn)
        self.add_item(buttons.add_items_btn)
        self.add_item(buttons.delete_btn)
