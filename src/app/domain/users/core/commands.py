from uuid import UUID

from a8t_tools.bus.producer import TaskProducer
from a8t_tools.security.hashing import PasswordHashService
from fastapi import HTTPException
from loguru import logger

from app.domain.common import enums
from app.domain.common.models import PasswordResetCode
from app.domain.common.schemas import IdContainer
from app.domain.users.core import schemas
from app.domain.users.core.queries import (
    UserRetrieveByCodeQuery,
    UserRetrieveByEmailQuery,
)
from app.domain.users.core.repositories import UpdatePasswordRepository, UserRepository
from app.domain.users.core.schemas import EmailForCode
from app.domain.users.registration.hi import send_password_reset_email


class UpdatePasswordRequestCommand:
    def __init__(
        self,
        user_retrieve_by_email_query: UserRetrieveByEmailQuery,
        repository: UpdatePasswordRepository,
    ):
        self.user_retrieve_by_email_query = user_retrieve_by_email_query
        self.repository = repository

    async def __call__(self, payload: schemas.EmailForCode) -> EmailForCode:
        email = payload.email
        user_internal = await self.user_retrieve_by_email_query(email)

        user_id = user_internal.id
        code = PasswordResetCode.generate_code()

        password_reset_code = schemas.PasswordResetCode(
            user_id=user_id,
            code=code,
        )

        await self.repository.delete_code(user_id)
        await self.repository.create_update_password(password_reset_code)
        await send_password_reset_email(email, code)

        return EmailForCode(email=email)


class UserPartialUpdateCommand:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(
        self, user_id: UUID, password_hash: str
    ) -> schemas.UserDetailsFull:
        payload = schemas.UserPartialUpdate(password_hash=password_hash)
        await self.user_repository.partial_update_user(user_id, payload)
        user = await self.user_repository.get_user_by_filter_or_none(
            schemas.UserWhere(id=user_id)
        )

        assert user
        return schemas.UserDetailsFull.model_validate(user)


class UpdatePasswordConfirmCommand:
    def __init__(
        self,
        user_retrieve_by_email_query: UserRetrieveByEmailQuery,
        user_retrieve_by_code_query: UserRetrieveByCodeQuery,
        repository: UserRepository,
        user_partial_update_command: UserPartialUpdateCommand,
        password_hash_service: PasswordHashService,
    ):
        self.user_retrieve_by_email_query = user_retrieve_by_email_query
        self.user_retrieve_by_code_query = user_retrieve_by_code_query
        self.repository = repository
        self.user_partial_update_command = user_partial_update_command
        self.password_hash_service = password_hash_service

    async def __call__(self, payload: schemas.UpdatePasswordConfirm) -> None:
        email = payload.email
        user_internal = await self.user_retrieve_by_email_query(email)
        if not user_internal:
            raise HTTPException(status_code=404, detail="User not found")

        code = payload.code
        code_internal = await self.user_retrieve_by_code_query(code)
        if not code_internal:
            raise HTTPException(status_code=404, detail="Invalid or expired code")

        user_id = user_internal.id
        user_id_by_code = code_internal.user_id

        if user_id != user_id_by_code:
            raise HTTPException(status_code=400, detail="Code does not match user")

        print("USER_ID: ", user_id)
        print("user_id_by_code: ", user_id_by_code)

        password_hash = await self.password_hash_service.hash(payload.password)
        await self.user_partial_update_command(user_id, password_hash)


class UserCreateCommand:
    def __init__(
        self,
        user_repository: UserRepository,
        task_producer: TaskProducer,
    ):
        self.user_repository = user_repository
        self.task_producer = task_producer

    async def __call__(self, payload: schemas.UserCreate) -> schemas.UserDetailsFull:
        user_id_container = await self.user_repository.create_user(
            schemas.UserCreateFull(
                status=enums.UserStatuses.unconfirmed,
                **payload.model_dump(),
            )
        )
        logger.info(f"User created: {user_id_container.id}")
        await self._enqueue_user_activation(user_id_container)
        user = await self.user_repository.get_user_by_filter_or_none(
            schemas.UserWhere(id=user_id_container.id)
        )
        assert user

        return schemas.UserDetailsFull.model_validate(user)

    async def _enqueue_user_activation(self, user_id_container: IdContainer) -> None:
        await self.task_producer.fire_task(
            enums.TaskNames.activate_user,
            queue=enums.TaskQueues.main_queue,
            user_id_container_dict=user_id_container.json_dict(),
        )


class UserActivateCommand:
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def __call__(self, user_id: UUID) -> None:
        await self.repository.set_user_status(user_id, enums.UserStatuses.active)
