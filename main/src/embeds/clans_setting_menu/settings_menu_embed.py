from discord import Embed, Colour


class SettingsMenu(object):
    def __init__(self):
        self._embed = Embed(
            title='Управління кланами',
            color=Colour(0x292b2f),
            description=f'***```Нажми на наступні кнопки, щоб керувати кланом або його учасниками\n'
                        f'1 - Запросити людину до клану\n'
                        f'2 - Вигнати людину з клану```***'
        )

    @property
    def embed(self):
        return self._embed
