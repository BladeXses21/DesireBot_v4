from enum import Enum, unique


@unique
class EnumEventList(Enum):
    # events
    alias = 'Шляпа'
    code_names = 'Code names'
    Brawlhalla = 'Brawlhalla'
    dota_2 = 'Dota 2'
    CS_GO = 'CS:GO'
    Viewing_something = 'Просмотр чего-либо'
    Puzzles = 'Пазлы'
    Fool = 'Дурак'
    Endless = 'Без остановки'
    Spy = 'Шпион'
    Brawl_Stars = 'Brawl Stars'
    TikTok = 'ТикТок'
    sheep = 'Овечки'
    Secret_Hitler = 'Секретный Гитлер'
    broken_phone = 'Сломанный телефон'
    Truth_or_Dare = 'Правда или действие'
    Hearthstone = 'Hearthstone'
    Solo = 'Соло'
    Who_am_I = 'Кто я'
    Cow = 'Корова'
    JackBox = 'JackBox'
    My_own_game = 'Своя игра'
    Bunker = 'Бункер'
    Poker = 'Покер'
    Monopoly = 'Монополия'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))