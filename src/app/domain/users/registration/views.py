from dependency_injector import wiring
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.domain.users.core.schemas import UserDetails, UserCredentialsRegist, EmailForCode, VerificationCode
from app.domain.users.registration.commands import UserRegisterCommand, UserEmailVerificationRequestCommand, \
    UserEmailVerificationConfirmCommand
from app.domain.users.registration.hi import send_hello

router = APIRouter()


@router.post(
    "/email/verification/request",
    response_model=None,
)
@wiring.inject
async def email_verification_code_request(
        payload: EmailForCode,
        command: UserEmailVerificationRequestCommand = Depends(
            wiring.Provide[Container.user.email_verification_request_command]),
):
    user_details = await command(payload)
    return user_details


@router.post(
    "/email/verification/confirm",
    status_code=status.HTTP_200_OK,
)
@wiring.inject
async def email_verification_code_confirm(
        payload: VerificationCode,
        command: UserEmailVerificationConfirmCommand = Depends(
            wiring.Provide[Container.user.email_verification_confirm_command]),
):
    user_details = await command(payload)
    if user_details:
        return {"message": "Код был удален"}
    else:
        print(payload)
        return {"message": "Код не найден"}


@router.post(
    "/registration",
    response_model=UserDetails,
)
@wiring.inject
async def register(
        payload: UserCredentialsRegist,
        command: UserRegisterCommand = Depends(wiring.Provide[Container.user.register_command]),
) -> UserDetails:
    user_details = await command(payload)
    await send_hello(user_details)
    return user_details
