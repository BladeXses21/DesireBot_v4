# Токен бота
from clan_event.inventory_types.hero_inventory import HeroInventory

Token = 'ODY2MDUwNzkzMzAwMDMzNTk2.YPM6pw.ydkfdaQT_hMroG5vYEXFJUpF8qg'

# MongoDb token
# BladeXses DB
# MongoToken = 'mongodb+srv://DesireBot:kopanura200121@cluster0.c1j11.mongodb.net/DesireBot?retryWrites=true&w=majority'
# DzianTao DB
MongoToken = 'mongodb+srv://DesireBot:PiLeJcaVFhesIe02@cluster0.e9eia.mongodb.net/DesireBotDB?retryWrites=true&w=majority'

# ID сервера
ClANS_GUILD_ID = 866061390313029662

# User ids
USER_ID = 450361269128790026

# Префикс бота
PREFIX = '.'

# Стафф роли
ADMIN_ROLE = 882637418249981993
MODER_ROLE = 882645477512859709

# Для кланов
CLANS = {
    'CLAN_CHAT': 948703886636646470,
    'CLAN_VOICE_CATEGORY': 952256288191037531,
    'CLAN_TEXT_CATEGORY': 952256343153213570,
    'CLAN_AVATAR_CHANGE': 2000,
    'CLAN_CREATE_COST': 15000,
    'CHANGE_NAME_COST': 5000,
    'CHANGE_COLOR_COST': 3000,
    'CLAN_5_SLOTS_COST': 1500,
    'CLAN_CONSLIGER_COST': 3000,
    'CLAN_START_MEMBER_SLOT': 25,
    'CLAN_MAX_MEMBER_SLOT': 150
}

CLANS_ROLES = {
    'CLAN_LEADER_ROLE_ID': 887496800699830302,
    'CLAN_CONSLIGER_ROLE_ID': 899383949829230613,
    'CLAN_CONTROL_ROLE_ID': 948739416820711424,
    'LEADER_ROLE_NAME': 'clan leader',
    'CONSLIGER_ROLE_NAME': 'clan consliger',
    'CLAN_CONTROL_ROLE_NAME': 'clan control'
}

TIMELY = 20
EMOTION_COST = 20
START_MONEY = 200

NEW_HERO_START_HEALTH = 100
NEW_HERO_START_ATTACK = 1
NEW_HERO_START_INVENTORY = HeroInventory(10)
