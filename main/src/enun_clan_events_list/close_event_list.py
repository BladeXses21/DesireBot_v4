from enum import Enum, unique


@unique
class EnumCloseEventList(Enum):
    # events to close
    valorant = 'Valorant'
    dota_2 = 'Dota 2'
    cs_go = 'CS:GO'
    other = 'Другие'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
