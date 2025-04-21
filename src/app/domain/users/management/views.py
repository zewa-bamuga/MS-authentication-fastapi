from contextlib import asynccontextmanager
from uuid import UUID

from a8t_tools.db import pagination, sorting
from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from fastapi import APIRouter, Depends, Header

from app.api import deps
from app.containers import Container
from app.domain.users.core import schemas
from app.domain.users.core.commands import UserPartialUpdateCommand
from app.domain.users.core.queries import UsersByIdsQuery
from app.domain.users.management.commands import \
    UserManagementPartialUpdateCommand
from app.domain.users.management.queries import UserManagementListQuery

router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.patch(
    "/{user_id}",
    response_model=schemas.UserDetailsFull,
)
@wiring.inject
async def partial_update_user(
        user_id: UUID,
        payload: schemas.UserPasswordUpdate,
        command: UserPartialUpdateCommand = Depends(wiring.Provide[Container.user.partial_update_command]),
) -> schemas.UserDetailsFull:
    return await command(user_id, payload)


@router.post(
    "/by-ids",
    response_model=list[schemas.UserDetailsFull],
)
@wiring.inject
async def get_users_by_ids(
        body: schemas.UsersByIdsRequest,
        query: UsersByIdsQuery = Depends(wiring.Provide[Container.user.users_by_ids_query]),
) -> list[schemas.UserDetailsFull]:
    return await query(body.ids)


@router.get(
    "/get/students/list",
    response_model=pagination.CountPaginationResults[schemas.UserDetails],
)
@wiring.inject
async def get_students_list(
        token: str = Header(...),
        query: UserManagementListQuery = Depends(
            wiring.Provide[Container.user.management_list_query]
        ),
        pagination: pagination.PaginationCallable[schemas.UserDetails] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.UserDetails)
        ),
        sorting: sorting.SortingData[schemas.UserSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.UserSorts,
                schemas.UserSorts.created_at,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.UserDetails]:
    async with user_token(token):
        return await query(
            schemas.UserListRequestSchema(
                pagination=pagination,
                sorting=sorting,
                where=schemas.UserWhere(permissions="student"),
            )
        )
