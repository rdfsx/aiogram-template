from pathlib import Path
from typing import NamedTuple

from environs import Env


class Config(NamedTuple):
    __env = Env()
    __env.read_env()

    BASE_DIR = Path(__name__).resolve().parent.parent

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

    INFLUX_HOST = 'influxdb'
    INFLUX_PASSWORD = __env.str('INFLUXDB_USER_PASSWORD')
    INFLUX_USER = __env.str('INFLUXDB_USER')
    INFLUX_DB = __env.str('INFLUXDB_DB')

