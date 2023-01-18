import datetime
from pydantic import BaseModel, Field


class ObjectSchema(BaseModel):
    name: str
    description: str = ""
    wrnt: datetime.datetime
    master: str = None
    work: bool = False
    public: bool = False


class ObjectSchemaPatch(BaseModel):
    name: str | None = None
    description: str | None
    wrnt: datetime.datetime | None = None
    master: str | None = None
    work: bool | None = None
    public: bool | None = None