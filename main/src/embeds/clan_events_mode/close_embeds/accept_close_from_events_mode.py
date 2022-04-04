import time

from discord import Embed, Colour


class AcceptCloseFromEventMode(object):
    def __init__(self, clan_name: str, clan_name_two: str, event_name: str, event_mode, interaction, comment: str):
        self._embed = Embed(
            title=f'Ивент был успешно принят.',
            description=f'***```{event_mode}, взял(а) ивент```***',
            color=Colour(0xd5d5d5),
        )
        self._embed.add_field(name='Первый Клан:', value=f"***```{clan_name}```***", inline=False)
        self._embed.add_field(name='Второй Клан:', value=f"***```{clan_name_two}```***", inline=False)
        self._embed.add_field(name='Ивент:', value=f"***```{event_name}```***", inline=False)
        self._embed.add_field(name='Пользователь:', value=f'{interaction.user.mention}', inline=False)
        self._embed.add_field(name='Ведущий', value=f"{event_mode}", inline=False)
        self._embed.add_field(name='Коментарий:', value=f"***```{comment}```***", inline=False)
        self._embed.add_field(name='Время отправки запроса:', value=f'<t:{int(time.time())}>', inline=False)

    @property
    def embed(self):
        return self._embed
