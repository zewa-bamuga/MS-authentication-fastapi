from uuid import UUID

from a8t_tools.schemas.pydantic import APIModel


class IdContainer(APIModel):
    id: UUID


class IdContainerTables(APIModel):
    id: int
