import time

from discord import Embed, Colour


class CloseRequestEmbed(object):
    def __init__(self, clan_name: str, event_name: str, interaction, members_on_voice, comment: str):
        self._embed = Embed(
            title=f'Клан {clan_name}, вызвал вас на клоз по игре {event_name}.',
            description='***```Ожидает рассмотрения...```***',
            color=Colour(0xd5d5d5),
        )
        self._embed.add_field(name='Количество людей:', value=f"***```{members_on_voice}```***", inline=False)
        self._embed.add_field(name='Пользователь:', value=f'{interaction.user.mention}', inline=False)
        self._embed.add_field(name='Коментарий:', value=str(comment), inline=False)
        self._embed.add_field(name='Время отправки запроса:', value=f'<t:{int(time.time())}>', inline=False)

    @property
    def embed(self):
        return self._embed
