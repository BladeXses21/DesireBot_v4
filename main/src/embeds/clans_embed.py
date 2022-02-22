from discord import Embed, Colour


class DeleteEmbed(object):
    def __init__(self, clan_name: str):
        self._embed = Embed(
            color=Colour(0xffffff),
            description=f'***```Клан {clan_name} был успешно удален.```***'
        )
        self._embed.set_image(url='https://i.pinimg.com/originals/41/88/70/418870ce04e8d596d6af6558818e5519.gif')


class ZamAdd(object):
    def __init__(self, author, member, clan_name, zum_num):
        self._embed = Embed(
            color=Colour(0xffffff),
            description=f'{author}, вы назначили {member} заместителем в клане {clan_name}.\nОсталось слотов для местителя {zum_num}.'
        )

    @property
    def embed(self):
        return self._embed
