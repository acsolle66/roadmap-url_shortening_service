import secrets
import string
from datetime import datetime, timezone
from functools import partial
from typing import Annotated

from beanie import Document, Indexed, Replace, before_event
from pydantic import Field, HttpUrl


def generate_short_code():
    alnum = string.ascii_letters + string.digits
    return "".join(secrets.choice(alnum) for i in range(8))


class URLMap(Document):
    url: HttpUrl = Field(...)
    short_code: Annotated[str, Indexed(unique=True)] = Field(
        default_factory=generate_short_code
    )
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    updated_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    access_count: int = Field(default=0)

    @before_event(Replace)
    def updated_at_field(self):
        self.updated_at = datetime.now(timezone.utc)

    class Settings:
        name = "url_maps"
