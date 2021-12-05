from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class TimeBaseModel(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
