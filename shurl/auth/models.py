from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field


class User(Document):
    username: Annotated[str, Indexed(unique=True)] = Field(...)
    hashed_password: str = Field(...)

    class Settings:
        name = "users"
