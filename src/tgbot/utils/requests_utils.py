from typing import Any, Literal, Union

import aiohttp


async def send_request(
    url: str,
    timeout: int = 30,
    params: dict = None,
    method: Literal["GET", "PUT", "POST", "DELETE"] = "GET",
    response_type: Literal["json", "text"] = "json",
    headers: Any = None,
    data: Any = None,
    json: Any = None,
) -> Union[dict, str]:
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method, url, params=params, timeout=timeout, data=data, headers=headers, json=json
        ) as resp:
            return await getattr(resp, response_type)()
