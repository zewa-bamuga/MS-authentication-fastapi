from contextlib import asynccontextmanager

from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from dependency_injector.wiring import Provide
from fastapi import APIRouter, Body, Depends, Header
from starlette import status

from app.containers import Container
from app.domain.users.auth.commands import TokenRefreshCommand, UserAuthenticateCommand
from app.domain.users.auth.queries import UserProfileMeQuery
from app.domain.users.auth.schemas import TokenResponse
from app.domain.users.core import schemas
from app.domain.users.core.commands import (
    UpdatePasswordConfirmCommand,
    UpdatePasswordRequestCommand,
)
from app.domain.users.core.schemas import EmailForCode, UserCredentials, UserDetailsFull

router = APIRouter()


@router.post(
    "/authentication",
    response_model=TokenResponse,
)
@wiring.inject
async def authenticate(
    payload: UserCredentials,
    command: UserAuthenticateCommand = Depends(
        wiring.Provide[Container.user.authenticate_command]
    ),
) -> TokenResponse:
    return await command(payload)


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
@wiring.inject
async def update_refresh_token(
    refresh_token: str = Body(embed=True),
    command: TokenRefreshCommand = Depends(
        wiring.Provide[Container.user.refresh_token_command]
    ),
) -> TokenResponse:
    return await command(refresh_token)


@router.post(
    "/password/reset/request",
    response_model=None,
)
@wiring.inject
async def password_reset_request(
    payload: EmailForCode,
    command: UpdatePasswordRequestCommand = Depends(
        wiring.Provide[Container.user.update_password_request_command]
    ),
):
    return await command(payload)


@router.post(
    "/password/reset/confirm",
    status_code=status.HTTP_204_NO_CONTENT,
)
@wiring.inject
async def password_reset_confirm(
    payload: schemas.UpdatePasswordConfirm,
    command: UpdatePasswordConfirmCommand = Depends(
        wiring.Provide[Container.user.update_password_confirm_command]
    ),
) -> None:
    await command(payload)


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.get(
    "/me",
    response_model=UserDetailsFull,
)
@wiring.inject
async def get_me(
    token: str = Header(...),
    query: UserProfileMeQuery = Depends(Provide[Container.user.profile_me_query]),
) -> UserDetailsFull:
    async with user_token(token):
        return await query()
