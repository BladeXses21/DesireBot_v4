import time

from discord import Embed, Colour


class RequestEmbed(object):
    def __init__(self, clan_name: str, event_name: str, interaction, members_on_voice, clan_control_role):
        self._embed = Embed(
            title='Запрос на проведение ивента.',
            description='***```Ожидает рассмотрения...```***',
            color=Colour(0xd5d5d5),
        )
        self._embed.add_field(name='Клан:', value=f'***```{clan_name}```***', inline=False)
        self._embed.add_field(name='Количество людей:', value=f"***```{members_on_voice}```***", inline=False)
        self._embed.add_field(name='Ивент:', value=f"***```{event_name}```***", inline=False)
        self._embed.add_field(name='Пользователь:', value=f'{interaction.user.mention}', inline=False)
        self._embed.add_field(name='Время отправки тикета:', value=f'<t:{int(time.time())}>', inline=False)
        self._embed.add_field(name='Роботяги', value=clan_control_role, inline=False)
        self._embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/2022/4hv9xm/ukrainian-waving-flag-14.gif')

    @property
    def embed(self):
        return self._embed


