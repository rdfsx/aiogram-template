from __future__ import annotations

import asyncio
import logging
from typing import Any, AsyncGenerator, Awaitable, Callable, Iterable

from aiogram.exceptions import TelegramRetryAfter, TelegramUnauthorizedError

from src.tgbot.utils.exceptions import CancelBroadcastException

logger = logging.getLogger(__name__)


async def broadcast(
    chats: AsyncGenerator[int | Any],
    action: Callable[[int, Any, ...], Awaitable[Any, int]],
    counter: int | None = 0,
    attribute: str | None = None,
    **func_kwargs: Any,
) -> int:

    async for chat in chats:
        if attribute:
            chat_id = getattr(chat, attribute, None) or chat[attribute]
        else:
            chat_id = chat

        try:
            if counter is not None:
                counter = await action(chat_id, counter, **func_kwargs)
            else:
                await action(chat_id, **func_kwargs)

        except TelegramRetryAfter as e:
            logger.error(
                f"Target [ID:{chat_id}]: Flood limit is exceeded. "
                f"Sleep {e.retry_after} seconds."
            )
            await asyncio.sleep(e.retry_after)

        except TelegramUnauthorizedError as e:
            raise e

        except CancelBroadcastException:
            return counter

        except Exception as e:
            logger.error(e)

        await asyncio.sleep(0.05)

    return counter


async def from_iterable(it: Iterable) -> AsyncGenerator:
    for item in it:
        await asyncio.sleep(0)
        yield item
