import uuid

from app.domain.users.core import schemas
from app.domain.users.core.commands import UserPartialUpdateCommand
from app.domain.users.permissions.schemas import BasePermissions
from app.domain.users.permissions.services import UserPermissionService
from app.domain.users.registration.commands import UserRegisterCommand


class UserManagementCreateCommand:
    def __init__(
        self,
        permission_service: UserPermissionService,
        command: UserRegisterCommand,
    ) -> None:
        self.permission_service = permission_service
        self.command = command

    async def __call__(self, payload: schemas.UserCredentials) -> schemas.UserDetails:
        await self.permission_service.assert_permissions(BasePermissions.superuser)
        return await self.command(payload)


class UserManagementPartialUpdateCommand:
    def __init__(
        self,
        permission_service: UserPermissionService,
        command: UserPartialUpdateCommand,
    ) -> None:
        self.permission_service = permission_service
        self.command = command

    async def __call__(
        self, user_id: uuid.UUID, payload: schemas.UserPartialUpdateFull
    ) -> schemas.UserDetailsFull:
        await self.permission_service.assert_permissions(BasePermissions.superuser)
        return await self.command(user_id, payload)
