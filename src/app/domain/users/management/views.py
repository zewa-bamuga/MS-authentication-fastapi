from uuid import UUID

from dependency_injector import wiring
from fastapi import APIRouter, Depends

from app.api import deps
from app.containers import Container
from app.domain.users.core import schemas
from app.domain.users.management.commands import (
    UserManagementCreateCommand,
    UserManagementPartialUpdateCommand,
)
from app.domain.users.management.queries import (
    UserManagementListQuery,
    UserManagementRetrieveQuery,
)
from a8t_tools.db import pagination, sorting

router = APIRouter()
