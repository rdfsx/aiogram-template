import json
import logging
import time
from typing import Literal

from app.config import Config
from app.utils.api import send_request


class ChatbaseMessage:
    def __init__(self,
                 message: str,
                 user_id: str,
                 intent: str = '',
                 version: str = '',
                 api_key: str = Config.STATISTICS_TOKEN,
                 platform: str = 'tg',
                 msg_type: Literal['user', 'agent'] = 'user',
                 not_handled: bool = False,
                 time_stamp: int = None) -> None:
        self.api_key = api_key
        self.platform = platform
        self.message = message
        self.intent = intent
        self.version = version
        self.user_id = user_id
        self.not_handled = not_handled
        self.feedback = False
        self.time_stamp = time_stamp or self.get_current_timestamp()
        self.type = msg_type

    def to_json(self) -> str:
        return json.dumps(self, default=lambda i: i.__dict__)

    @staticmethod
    def get_current_timestamp() -> int:
        return int(round(time.time() * 1e3))

    @staticmethod
    def get_content_type() -> dict[str, str]:
        return {'Content-type': 'application/json', 'Accept': 'text/plain'}

    async def send(self) -> None:
        url = "https://chatbase.com/api/message"
        response = await send_request(url,
                                      method="POST",
                                      data=self.to_json(),
                                      headers=self.get_content_type(),
                                      response_type="text")
        logging.info(f"Chatbase response {response}")
