from discord.ui import View

from embeds.view.buttons import buttons


class ProfileView(View):
    def __init__(self, back_callback, inventory_callback):
        super().__init__(timeout=None)
        buttons.back_btn.callback = back_callback
        buttons.inventory_btn.callback = inventory_callback
        self.add_item(buttons.back_btn)
        self.add_item(buttons.inventory_btn)

    @staticmethod
    def disable_attack(disable: bool):
        buttons.attack_btn.disabled = disable
