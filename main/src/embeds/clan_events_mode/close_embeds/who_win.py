import time

from discord import Embed, Colour


class WinCloseFromEventMode(object):
    def __init__(self, clan_win: str, clan_name_two: str, event_name: str, event_mode):
        self._embed = Embed(
            title=f'Победа присуждается клану {clan_win}',
            color=Colour(0xd5d5d5),
        )
        self._embed.add_field(name='Победивший', value=f'***```{clan_win}```***')
        self._embed.add_field(name='Проигравший:', value=f"***```{clan_name_two}```***", inline=False)
        self._embed.add_field(name='Ивент:', value=f"***```{event_name}```***", inline=False)
        self._embed.add_field(name='Ведущий', value=f"{event_mode}", inline=False)
        self._embed.add_field(name='Потрачено времени:', value='ВРЕМЯ', inline=False)
        self._embed.add_field(name='Время отправки запроса:', value=f'<t:{int(time.time())}>', inline=False)

    @property
    def embed(self):
        return self._embed
