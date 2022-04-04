from discord.ui import View

from embeds.view.buttons import buttons


class BossesView(View):
    def __init__(self, back_callback, up_callback, down_callback, choose_callback):
        super().__init__(timeout=None)
        buttons.back_btn.callback = back_callback
        buttons.up_btn.callback = up_callback
        buttons.down_btn.callback = down_callback
        buttons.choose_btn.callback = choose_callback
        self.add_item(buttons.back_btn)
        self.add_item(buttons.up_btn)
        self.add_item(buttons.down_btn)
        self.add_item(buttons.choose_btn)

