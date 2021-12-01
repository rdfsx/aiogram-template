from pydantic import Field

from app.models.base import BaseModel


class ChatModel(BaseModel):
    id: int = Field(alias="_id")
    type: str = Field(...)

    class Collection:
        name = "ChatModel"
