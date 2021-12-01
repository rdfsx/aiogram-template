from enum import Enum

from pydantic import Field

from app.models.base import BaseModel


class UserRoles(str, Enum):
    new = 'new'
    user = 'user'
    admin = 'admin'


class UserModel(BaseModel):
    id: int = Field(alias="_id")
    language: str = 'en'
    real_language: str = 'en'
    role: UserRoles = Field(default=UserRoles.new)
    status: str = 'member'

    class Collection:
        name = "UserModel"
