import time

from discord import Embed, Colour


class RequestPassEmbed(object):
    def __init__(self, clan_name: str, event_name: str, create_request_member, clan_control, event_pass):
        self._embed = Embed(
            title='Ивент был успешно завершен.',
            description=f'***```{clan_control}, завершил ивент```***',
            color=Colour(0xd5d5d5)
        )
        self._embed.add_field(name='Клан:', value=f'***```{clan_name}```***', inline=False)
        self._embed.add_field(name='Запросил ивент:', value=f"***```{create_request_member}```***", inline=False)
        self._embed.add_field(name='Ивент:', value=f"***```{event_name}```***", inline=False)
        self._embed.add_field(name='Ведущий ивента', value=f"***```{clan_control}```***", inline=False)
        self._embed.add_field(name='Суммарное время ивента', value=f"***```{event_pass}```***", inline=False)
        self._embed.add_field(name='Время окончания ивента:', value=f'<t:{int(time.time())}>', inline=False)
        self._embed.set_thumbnail(url='https://acegif.com/wp-content/uploads/2022/4hv9xm/ukrainian-waving-flag-14.gif')

    @property
    def embed(self):
        return self._embed
