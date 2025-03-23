from uuid import UUID

from a8t_tools.db.pagination import Paginated

from app.domain.users.core.queries import UserListQuery, UserRetrieveQuery
from app.domain.users.core.schemas import User, UserDetailsFull, UserListRequestSchema
from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.permissions.services import UserPermissionService


class UserManagementListQuery:
    def __init__(
        self, permission_service: UserPermissionService, query: UserListQuery
    ) -> None:
        self.query = query
        self.permission_service = permission_service

    async def __call__(self, payload: UserListRequestSchema) -> Paginated[User]:
        await self.permission_service.assert_permissions(BasePermissions.superuser)
        return await self.query(payload)


class UserManagementRetrieveQuery:
    def __init__(
        self,
        query: UserRetrieveQuery,
        permission_service: UserPermissionService,
    ) -> None:
        self.query = query
        self.permission_service = permission_service

    async def __call__(self, payload: UUID) -> UserDetailsFull:
        await self.permission_service.assert_permissions(BasePermissions.superuser)
        user = await self.query(payload)
        return UserDetailsFull.model_validate(user)
