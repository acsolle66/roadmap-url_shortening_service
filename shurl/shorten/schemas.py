from datetime import datetime

from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, Field, HttpUrl


class URLMapCreate(BaseModel):
    url: HttpUrl = Field(...)


class URLMapUpdate(BaseModel):
    url: HttpUrl = Field(...)


class URLMapResponse(BaseModel):
    id: PydanticObjectId
    url: HttpUrl
    short_code: str = Field(serialization_alias="shortCode")
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")


class URLMapResponseWithStats(URLMapResponse):
    access_count: int = Field(serialization_alias="accessCount")
