from typing import Literal, Any, Union

import aiohttp


async def send_request(url: str,
                       timeout: int = 30,
                       params: dict = None,
                       session: aiohttp.ClientSession = None,
                       method: Literal["GET", "PUT", "POST", "DELETE"] = "GET",
                       response_type: Literal["json", "text"] = "json",
                       headers: Any = None,
                       data: Any = None,
                       json: Any = None) -> Union[dict, str]:
    if not session:
        session = aiohttp.ClientSession()
    async with session.request(method,
                               url,
                               params=params,
                               timeout=timeout,
                               data=data,
                               headers=headers,
                               json=json) as resp:
        result = await getattr(resp, response_type)()
    if not session:
        await session.close()
    return result
