from discord import Embed, Colour


class DeleteEmbed(object):
    def __init__(self, clan_name: str, img_url: str):
        self._embed = Embed(
            color=Colour(0x292b2f),
            description=f'***```Клан {clan_name} был успешно удален.```***'
        )
        if img_url:
            self._embed.set_thumbnail(url=img_url)

    @property
    def embed(self):
        return self._embed

class ZamEmbed(object):
    def __init__(self, author, member, clan_name, zum_num):
        self._embed = Embed(
            color=Colour(0x292b2f),
            description=f'***```{author}, вы назначили {member} заместителем в клане {clan_name}.\nОсталось слотов для заместителя {zum_num - 1}.```***'
        )

    @property
    def embed(self):
        return self._embed
