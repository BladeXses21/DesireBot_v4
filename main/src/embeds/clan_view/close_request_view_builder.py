import discord
from discord.ui import View, Button


class CloseRequestViewBuilder:
    def __init__(self):
        self.accept_request = Button(style=discord.ButtonStyle.secondary, label='Принять вызов', emoji='✔')
        self.decline_request = Button(style=discord.ButtonStyle.secondary, label='Отклонить вызов', emoji='❌')

        self.event_mode_accept_request = Button(style=discord.ButtonStyle.green, label='Взять клоз', emoji='✔')
        self.first_clan_victory = Button(style=discord.ButtonStyle.secondary, label='Clan first', emoji='🎀')
        self.second_clan_victory = Button(style=discord.ButtonStyle.secondary, label='Clan second', emoji='🎀')
        self.event_mode_decline_request = Button(style=discord.ButtonStyle.red, label='Убрать клоз', emoji='❌')

    def create_close_request_view(self) -> View:
        create_close_view = View(timeout=None)
        create_close_view.add_item(self.accept_request)
        create_close_view.add_item(self.decline_request)
        return create_close_view

    def button_for_events_mode(self) -> View:
        event_mode_accept_request = View(timeout=None)
        event_mode_accept_request.add_item(self.event_mode_accept_request)
        event_mode_accept_request.add_item(self.event_mode_decline_request)
        return event_mode_accept_request

    def who_wining_close(self, clan_name_one, clan_name_two) -> View:
        warring_clans = View(timeout=None)
        self.first_clan_victory.label = str(clan_name_one)
        self.second_clan_victory.label = str(clan_name_two)
        warring_clans.add_item(self.first_clan_victory)
        warring_clans.add_item(self.second_clan_victory)
        return warring_clans


close_request_view_builder = CloseRequestViewBuilder()
