import math
from datetime import datetime
from typing import Any, AsyncIterator, Mapping, Optional, Type, Union

from beanie import Document, Insert, Replace, SaveChanges, before_event
from beanie.odm.documents import DocType
from pydantic import Field


class TimeBaseModel(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @before_event([Insert, Replace, SaveChanges])
    def set_updated_at(self):
        self.updated_at = datetime.utcnow()

    @classmethod
    async def safe_find(
        cls: Type["DocType"],
        *conditions: Union[Mapping[str, Any], bool],
        limit: int = 1000,
        sort_by: str = "created_at",
        **kwargs,
    ) -> AsyncIterator["DocType"]:
        count = await cls.find(*conditions, **kwargs).count()

        for i in range(math.ceil(count / limit)):
            async for obj in cls.find(*conditions, **kwargs).sort(sort_by).limit(limit).skip(
                i * limit
            ):
                yield obj
