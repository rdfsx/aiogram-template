from datetime import datetime
from enum import Enum

from beanie import before_event, Insert, Replace, SaveChanges
from pydantic import Field

from app.models.base import TimeBaseModel


class UserRoles(str, Enum):
    new = 'new'
    user = 'user'
    admin = 'admin'


class UserModel(TimeBaseModel):
    id: int = Field(...)
    language: str = 'en'
    real_language: str = 'en'
    role: UserRoles = Field(default=UserRoles.new)
    status: str = 'member'

    class Collection:
        name = "UserModel"

    @before_event([Insert, Replace, SaveChanges])
    def set_updated_at(self):
        self.updated_at = datetime.utcnow()
