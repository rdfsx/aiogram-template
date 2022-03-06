from __future__ import annotations

import asyncio
import logging
from asyncio import Lock
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Any, Awaitable, Iterable, DefaultDict, Hashable

from aiogram.exceptions import TelegramRetryAfter

from app.utils.exceptions import BroadcastLockException

logger = logging.getLogger(__name__)


async def broadcast_smth(chats: AsyncGenerator[int | Any],
                         action: Callable[[int, Any, ...], Awaitable[Any, int]],
                         with_counter: bool = True,
                         attribute: str | None = None,
                         **func_kwargs: Any) -> int:
    i = 0

    async for chat in chats:
        if attribute:
            chat_id = getattr(chat, attribute)
        else:
            chat_id = chat

        try:
            if with_counter:
                i += await action(chat_id, i, **func_kwargs)
            else:
                await action(chat_id, **func_kwargs)

        except TelegramRetryAfter as e:
            logger.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. "
                         f"Sleep {e.retry_after} seconds.")
            await asyncio.sleep(e.retry_after)

        except Exception as e:
            logger.error(e)

        await asyncio.sleep(0.05)

    return i


async def from_iterable(it: Iterable) -> AsyncGenerator:
    for item in it:
        await asyncio.sleep(0)
        yield item


class MemoryBroadcastBotLocker:
    def __init__(self) -> None:
        self._locks: DefaultDict[Hashable, Lock] = defaultdict(Lock)

    @asynccontextmanager
    async def lock(self, bot_id: int) -> AsyncGenerator[None, None]:
        if self.is_exist(bot_id):
            raise BroadcastLockException

        lock = self._locks[bot_id]
        async with lock:
            yield

        self.delete(bot_id)

    def is_exist(self, bot_id: int) -> bool:
        return True if self._locks.get(bot_id, None) else False

    def delete(self, bot_id: int) -> None:
        self._locks.pop(bot_id)

    def close(self) -> None:
        self._locks.clear()

    def __del__(self):
        self.close()
