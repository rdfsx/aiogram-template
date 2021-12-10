from datetime import datetime
from typing import Optional

from beanie import Document, before_event, Insert, Replace, SaveChanges
from pydantic import Field


class TimeBaseModel(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @before_event([Insert, Replace, SaveChanges])
    def set_updated_at(self):
        self.updated_at = datetime.utcnow()
