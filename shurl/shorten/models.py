import secrets
import string
from datetime import datetime, timezone
from functools import partial
from typing import Annotated

from beanie import Document, Indexed, Replace, before_event
from pydantic import Field


def generate_short_code():
    alnum = string.ascii_letters + string.digits
    return "".join(secrets.choice(alnum) for i in range(8))


class URLMap(Document):
    url: str = Field(...)
    short_code: Annotated[str, Indexed(unique=True)] = Field(
        default_factory=generate_short_code,
        serialization_alias="shortCode",
    )
    created_at: datetime = Field(
        default_factory=partial(datetime.now, tz=timezone.utc),
        serialization_alias="createdAt",
    )
    updated_at: datetime = Field(
        default_factory=partial(datetime.now, tz=timezone.utc),
        serialization_alias="updatedAt",
    )
    acces_count: int = Field(default=0, serialization_alias="accesCount")

    @before_event(Replace)
    def updated_at_field(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "url_maps"
