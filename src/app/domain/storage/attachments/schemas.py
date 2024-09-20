import enum
from dataclasses import dataclass
from datetime import datetime
from typing import IO
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr

from app.domain.common.schemas import APIModel


class Attachment(APIModel):
    id: UUID
    name: str
    path: str
    uri: str | None = None
    created_at: datetime


@dataclass
class AttachmentCreate:
    name: str | None
    file: IO[bytes]


class AttachmentCreateFull(APIModel):
    name: str
    path: str
    uri: str


class AttachmentSorts(enum.StrEnum):
    id = enum.auto()
    name = enum.auto()  # type: ignore [assignment]
    uri = enum.auto()
    created_at = enum.auto()


@dataclass
class AttachmentListRequestSchema:
    pagination: pg.PaginationCallable[Attachment] | None = None
    sorting: sr.SortingData[AttachmentSorts] | None = None
