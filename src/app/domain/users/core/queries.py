from uuid import UUID

from a8t_tools.db.pagination import Paginated

from app.domain.common.exceptions import NotFoundError
from app.domain.users.core import schemas
from app.domain.users.core.repositories import (UpdatePasswordRepository,
                                                UserRepository)
from app.domain.users.core.schemas import UserDetailsFull


class EmailRetrieveQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, user_email: str) -> schemas.UserInternal:
        result = await self.repository.get_user_by_filter_by_email_or_none(
            schemas.UserWhere(email=user_email)
        )
        if not result:
            raise NotFoundError()
        return schemas.UserInternal.model_validate(result)


class UserRetrieveByUsernameQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, firstname: str) -> schemas.UserInternal | None:
        return await self.repository.get_user_by_filter_or_none(
            schemas.UserWhere(firstname=firstname)
        )


class UserRetrieveByEmailQuery:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, email: str) -> schemas.UserInternal | None:
        try:
            user_internal = (
                await self.user_repository.get_user_by_filter_by_email_or_none(
                    schemas.UserWhere(email=email)
                )
            )
        except Exception as e:
            print("не попал:", e)
            user_internal = None

        return user_internal


class UserRetrieveByCodeQuery:
    def __init__(
            self,
            update_password_repository: UpdatePasswordRepository,
            user_repository: UserRepository,
    ):
        self.update_password_repository = update_password_repository
        self.user_repository = user_repository

    async def __call__(self, code: str) -> schemas.PasswordResetCode:
        password_reset_code_internal = await self.update_password_repository.get_password_reset_code_by_code_or_none(
            schemas.PasswordResetCodeWhere(code=code)
        )

        if password_reset_code_internal is None:
            password_reset_code_internal = (
                await self.user_repository.get_password_reset_code_by_code_or_none(
                    schemas.PasswordResetCodeWhere(code=code)
                )
            )

        print("выполняется после password_reset_code_internal")

        return password_reset_code_internal


class UserRetrieveQuery:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID) -> schemas.UserInternal:
        result = await self.user_repository.get_user_by_filter_or_none(
            schemas.UserWhere(id=user_id)
        )
        if not result:
            raise NotFoundError()
        return schemas.UserInternal.model_validate(result)


class UserListQuery:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(
            self, payload: schemas.UserListRequestSchema
    ) -> Paginated[schemas.User]:
        return await self.user_repository.get_users(
            pagination=payload.pagination,
            sorting=payload.sorting,
            where=payload.where,
        )


class UsersByIdsQuery:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def __call__(self, ids: list[UUID]) -> list[UserDetailsFull]:
        users = await self.user_repository.get_users_by_ids(ids)
        return [UserDetailsFull.model_validate(user) for user in users]
