import math
from datetime import datetime
from typing import Optional, Union, Mapping, Any, Type, AsyncIterator

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
        sort_by: str = "created_at",
        limit: int = 100,
    ) -> AsyncIterator["DocType"]:
        statement = cls.find(*conditions)

        count = await statement.count()

        for i in range(math.ceil(count / limit)):
            async for obj in (
                statement.sort(sort_by).limit(limit).skip(count if i == 0 else i * limit)
            ):
                yield obj
