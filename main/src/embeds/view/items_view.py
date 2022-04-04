from discord.ui import View

from embeds.view.buttons import buttons


class ItemsView(View):
    def __init__(self, back_callback, detail_callback, delete_callback):
        super().__init__(timeout=None)
        buttons.back_btn.callback = back_callback
        buttons.detail.callback = detail_callback
        buttons.delete_btn.callback = delete_callback
        self.add_item(buttons.back_btn)
        self.add_item(buttons.detail)
        self.add_item(buttons.delete_btn)