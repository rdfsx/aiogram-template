from typing import NamedTuple

from environs import Env


class Config(NamedTuple):
    __env = Env()
    __env.read_env()

    BOT_TOKEN = __env.str('BOT_TOKEN')

    ADMINS = __env.list('ADMIN_ID')

    MONGODB_DATABASE = __env.str('MONGODB_DATABASE')
    MONGODB_USERNAME = __env.str('MONGODB_USERNAME')
    MONGODB_PASSWORD = __env.str('MONGODB_PASSWORD')
    MONGODB_HOSTNAME = __env.str('MONGODB_HOSTNAME')
    MONGODB_PORT = __env.str('MONGODB_PORT')
    MONGODB_URI = 'mongodb://'

    if MONGODB_USERNAME and MONGODB_PASSWORD:
        MONGODB_URI += f"{MONGODB_USERNAME}:{MONGODB_PASSWORD}@"
    MONGODB_URI += f"{MONGODB_HOSTNAME}:{MONGODB_PORT}"
