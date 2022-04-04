from discord import Interaction
from discord.types.embed import Embed
from discord.ui import View

from embeds.view.buttons import buttons


class FightView(View):
    def __init__(self, attack_callback, profile_callback):
        super().__init__(timeout=None)
        buttons.attack_btn.callback = attack_callback
        buttons.profile_btn.callback = profile_callback
        self.add_item(buttons.attack_btn)
        self.add_item(buttons.profile_btn)

    @staticmethod
    def disable_attack(disable: bool):
        buttons.attack_btn.disabled = disable
