from a8t_tools.security.permissions import PermissionResolver

from app.domain.common.enums import AuthErrorCodes
from app.domain.common.exceptions import AuthError, NotFoundError, UserPermissionError
from app.domain.users.auth.queries import CurrentUserTokenPayloadQuery
from app.domain.users.permissions.queries import UserPermissionListQuery


class UserPermissionService:
    def __init__(
            self,
            query: UserPermissionListQuery,
            current_user_token_payload_query: CurrentUserTokenPayloadQuery,
    ) -> None:
        self.query = query
        self.current_user_token_payload_query = current_user_token_payload_query

    async def has_permissions(self, permissions: PermissionResolver) -> bool:
        token_payload = await self.current_user_token_payload_query()
        if not token_payload:
            return False
        try:
            user_scopes = await self.query(token_payload.sub)
        except NotFoundError:
            raise AuthError(code=AuthErrorCodes.invalid_token)
        return permissions.resolve(user_scopes)

    async def assert_permissions(self, permissions: PermissionResolver) -> None:
        print("Выполняется проверка permissions")
        if not await self.has_permissions(permissions):
            raise UserPermissionError()
