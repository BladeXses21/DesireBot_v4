import time

from discord import Embed, Colour


class DeclineCloseEmbed(object):
    def __init__(self, clan_name_decline: str, member_decline):
        self._embed = Embed(
            title=f'Клан {clan_name_decline} отклонил вызов.',
            description='***```Пытка не пытка...```***',
            color=Colour(0xd5d5d5),
        )
        self._embed.add_field(name='Отклонил пользователь:', value=member_decline, inline=False)
        self._embed.add_field(name='Время отклонения запроса:', value=f'<t:{int(time.time())}>', inline=False)

    @property
    def embed(self):
        return self._embed


class DeclineResponseCloseEmbed(object):
    def __init__(self, clan_name_request, member_decline):
        self._embed = Embed(
            title=f'Вы отклонили запрос на клоз от клана:{clan_name_request}',
            description='***```Жаль..очень жаль.```***',
            color=Colour(0xd5d5d5),
        )
        self._embed.add_field(name='Отклонил пользователь:', value=member_decline, inline=False)
        self._embed.add_field(name='Время отклонения запроса:', value=f'<t:{int(time.time())}>', inline=False)

    @property
    def embed(self):
        return self._embed
