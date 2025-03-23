import json
import uuid
from typing import Any

from a8t_tools.security import tokens
from a8t_tools.security.hashing import PasswordHashService

from app.domain.common import enums
from app.domain.common.exceptions import AuthError
from app.domain.users.auth.queries import TokenPayloadQuery
from app.domain.users.auth.repositories import TokenRepository
from app.domain.users.auth.schemas import TokenInfo, TokenPayload, TokenResponse
from app.domain.users.core.queries import UserRetrieveByEmailQuery, UserRetrieveQuery
from app.domain.users.core.schemas import UserCredentials, UserInternal


class TokenCreateCommand:
    def __init__(
        self,
        repository: TokenRepository,
        jwt_service: tokens.JwtServiceBase,
    ) -> None:
        self.repository = repository
        self.jwt_service = jwt_service

    async def __call__(self, user: UserInternal) -> TokenResponse:
        token_id = uuid.uuid4()
        await self.repository.create_token_info(
            TokenInfo(user_id=user.id, token_id=token_id)
        )

        return await self._get_token_data(user, token_id)

    async def _get_token_data(
        self, user: UserInternal, token_id: uuid.UUID
    ) -> TokenResponse:
        access_token = await self.jwt_service.encode(
            await self._format_access_token_payload(user), "access"
        )
        refresh_token = await self.jwt_service.encode(
            await self._format_refresh_token_payload(token_id), "refresh"
        )

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def _format_access_token_payload(self, user: UserInternal) -> Any:
        return json.loads(TokenPayload(sub=user.id).model_dump_json())

    async def _format_refresh_token_payload(self, token_id: uuid.UUID) -> Any:
        return json.loads(TokenPayload(sub=token_id).model_dump_json())


class TokenRefreshCommand:
    def __init__(
        self,
        repository: TokenRepository,
        query: TokenPayloadQuery,
        command: TokenCreateCommand,
        user_query: UserRetrieveQuery,
    ) -> None:
        self.repository = repository
        self.query = query
        self.command = command
        self.user_query = user_query

    async def __call__(self, refresh_token: str) -> TokenResponse:
        try:
            token_payload: TokenPayload = await self.query(refresh_token)
        except AuthError as e:
            token_payload: TokenPayload = await self.query(
                refresh_token, validate=False
            )
            await self.repository.delete_tokens(token_payload.sub)
            raise e
        user_tokens = await self.repository.get_token_info(token_payload.sub)

        if not user_tokens or token_payload.sub != user_tokens.token_id:
            raise AuthError(code=enums.AuthErrorCodes.invalid_token)

        await self.repository.delete_tokens(token_payload.sub)

        return await self.command(await self.user_query(user_tokens.user_id))


class UserAuthenticateCommand:
    def __init__(
        self,
        get_user_by_email: UserRetrieveByEmailQuery,
        password_hash_service: PasswordHashService,
        command: TokenCreateCommand,
    ) -> None:
        self.get_user_by_email = get_user_by_email
        self.password_hash_service = password_hash_service
        self.command = command

    async def __call__(self, payload: UserCredentials) -> TokenResponse:
        user = await self.get_user_by_email(payload.email)

        if not user or not await self.password_hash_service.verify(
            payload.password,
            user.password_hash,
        ):
            raise AuthError(code=enums.AuthErrorCodes.invalid_credentials)
        return await self.command(user)
