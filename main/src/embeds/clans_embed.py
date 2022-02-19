from discord import Embed, Colour


class DeleteEmbed(object):
    def __init__(self, author, clan_name):
        self._embed = Embed(
            color=Colour(0xffffff),
            description=f'{author}***```Клан {clan_name} был успешно удален.```***'
        )
        self._embed.set_image(url='https://anime-chan.me/uploads/posts/2013-07/1372650141_aiura.gif')


class ZamAdd(object):
    def __init__(self, author, member, clan_name, zum_num):
        self._embed = Embed(
            color=Colour(0xffffff),
            description=f'{author}, вы назначили {member} заместителем в клане {clan_name}.\nОсталось слотов для местителя {zum_num}.'
        )

    @property
    def embed(self):
        return self._embed
