import typing
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class RepairFlag(str, Enum):
    WORK = 'WORK'
    WASH = 'WAHING'


class PlaceSchema(BaseModel):
    id: UUID = Field(alias='_id')
    repair_flag: RepairFlag
    name: str
    description: str
    inWork: bool
    objects: typing.List[UUID]

