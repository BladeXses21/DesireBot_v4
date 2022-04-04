from discord.ui import View

from embeds.view.buttons import buttons


class AdminMenuView(View):
    def __init__(self, enemies_callback, items_callback, heroes_callback):
        super().__init__(timeout=None)
        buttons.enemies_btn.callback = enemies_callback
        buttons.items_btn.callback = items_callback
        buttons.heroes_btn.callback = heroes_callback
        self.add_item(buttons.enemies_btn)
        self.add_item(buttons.items_btn)
        self.add_item(buttons.heroes_btn)

