import time

from discord import Embed, Colour


class AcceptCloseEmbed(object):
    def __init__(self, clan_name_requesting: str, clan_name_accepted: str, event_name: str, member_request, member_accepted, comment: str):
        self._embed = Embed(
            title=f'Клан {clan_name_accepted}, одобрил приглошеник клана {clan_name_requesting}',
            description='***```Ожидает рассмотрения ивентёром...```***',
            color=Colour(0xd5d5d5),
        )
        self._embed.add_field(name='Название ивента:', value=f"***```{event_name}```***", inline=False)
        self._embed.add_field(name='Коментарий:', value=f'***```{comment}```***', inline=False)
        self._embed.add_field(name='Запросил пользователь:', value=member_request, inline=False)
        self._embed.add_field(name='Принял пользователь:', value=member_accepted, inline=False)
        self._embed.add_field(name='Время отправки запроса:', value=f'<t:{int(time.time())}>', inline=False)

    @property
    def embed(self):
        return self._embed
