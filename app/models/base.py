from datetime import datetime
from typing import Optional

from beanie import Document, before_event, Insert, Replace
from pydantic import Field


class BaseModel(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @before_event([Insert, Replace])
    def set_updated_at(self):
        self.updated_at = datetime.utcnow()
