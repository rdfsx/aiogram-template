from aiogram import Dispatcher
from aioinflux import InfluxDBClient

from .acl import ACLMiddleware
from .clocks import ClocksMiddleware
from .influxdb import InfluxDBMiddleware
from .locker import EventLockMiddleware
from .stats import StatsMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher, influx_client: InfluxDBClient):
    dp.message.middleware(ThrottlingMiddleware())
    # dp.callback_query.middlewares(ThrottlingMiddleware())
    dp.message.middleware(ClocksMiddleware())
    dp.callback_query.middleware(ClocksMiddleware())
    dp.message.middleware(EventLockMiddleware())
    dp.update.outer_middleware(ACLMiddleware())
    dp.update.middleware(InfluxDBMiddleware(influx_client))
    dp.message.middleware(StatsMiddleware())
    dp.callback_query.middleware(StatsMiddleware())
