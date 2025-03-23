from a8t_tools.security.hashing import PasswordHashService

from app.domain.common.models import EmailCode
from app.domain.users.core import schemas
from app.domain.users.core.commands import UserCreateCommand
from app.domain.users.core.repositories import EmailRpository
from app.domain.users.registration.hi import send_user_email_verification


class UserEmailVerificationRequestCommand:
    def __init__(
        self,
        repository: EmailRpository,
    ) -> None:
        self.repository = repository

    async def __call__(self, payload: schemas.EmailForCode) -> None:
        email = payload.email
        code = EmailCode.generate_code()

        create_verification_code = schemas.EmailVerificationCode(
            email=email,
            code=code,
        )

        await self.repository.email_deletion(email)
        await self.repository.create_code(create_verification_code)
        await send_user_email_verification(email, code)


class UserEmailVerificationConfirmCommand:
    def __init__(
        self,
        repository: EmailRpository,
    ) -> None:
        self.repository = repository

    async def __call__(self, payload: schemas.VerificationCode) -> None:
        code = payload.code

        await self.repository.code_deletion(code)


class UserRegisterCommand:
    def __init__(
        self,
        create_command: UserCreateCommand,
        password_hash_service: PasswordHashService,
    ) -> None:
        self.create_command = create_command
        self.password_hash_service = password_hash_service

    async def __call__(self, payload: schemas.UserCredentialsRegist) -> schemas.UserDetailsFull:
        return await self.create_command(
            schemas.UserCreate(
                firstname=payload.firstname,
                lastname=payload.lastname,
                email=payload.email,
                password_hash=(await self.password_hash_service.hash(payload.password)),
                avatar_attachment_id=None,
                permissions=payload.permissions,
            )
        )
