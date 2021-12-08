from datetime import datetime

from beanie import before_event, Insert, Replace, SaveChanges
from pydantic import Field

from app.models.base import TimeBaseModel


class ChatModel(TimeBaseModel):
    id: int = Field(...)
    type: str = Field(...)

    class Collection:
        name = "ChatModel"

    @before_event([Insert, Replace, SaveChanges])
    def set_updated_at(self):
        self.updated_at = datetime.utcnow()
