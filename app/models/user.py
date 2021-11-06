import json
from datetime import datetime
from enum import Enum

from odmantic import Field, Model


class UserRoles(str, Enum):
    new = 'new'
    user = 'user'
    admin = 'admin'


class UserModel(Model):
    id: int = Field(primary_field=True)
    language: str = 'en'
    role: UserRoles = Field(default=UserRoles.new)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        collection = "Users"
        json_loads = json.loads
        parse_doc_with_default_factories = True
