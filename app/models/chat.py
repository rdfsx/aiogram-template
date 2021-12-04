from pydantic import Field

from app.models.base import TimeBaseModel


class ChatModel(TimeBaseModel):
    id: int = Field(alias="_id")
    type: str = Field(...)

    class Collection:
        name = "ChatModel"
