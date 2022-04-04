from discord.ui import View

from embeds.view.buttons import buttons


class AddItemsView(View):
    def __init__(self, back_callback, up_callback, down_callback, add_callback, detail_callback):
        super().__init__(timeout=None)
        buttons.back_btn.callback = back_callback
        buttons.up_btn.callback = up_callback
        buttons.down_btn.callback = down_callback
        buttons.add_item_btn.callback = add_callback
        buttons.detail_btn.callback = detail_callback
        self.add_item(buttons.back_btn)
        self.add_item(buttons.up_btn)
        self.add_item(buttons.down_btn)
        self.add_item(buttons.detail_btn)
        self.add_item(buttons.add_item_btn)

    @staticmethod
    def disable_add_and_detail(disable: bool):
        buttons.attack_btn.disabled = disable
        buttons.detail_btn.disabled = disable
