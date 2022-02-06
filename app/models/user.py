from enum import Enum

from pydantic import Field
from pydantic.main import BaseModel

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
