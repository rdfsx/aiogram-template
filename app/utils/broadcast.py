from __future__ import annotations

import asyncio
import logging
from typing import AsyncGenerator, Callable, Any, Awaitable, Iterable

from aiogram.exceptions import TelegramRetryAfter

logger = logging.getLogger(__name__)


async def broadcast_smth(chats: AsyncGenerator[int] | Any,
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
