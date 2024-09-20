from contextlib import contextmanager
from contextvars import ContextVar

from a8t_tools.security import tokens

from app.domain.common import enums
from app.domain.common.exceptions import AuthError
from app.domain.users.auth import schemas
from app.domain.users.core.queries import UserRetrieveQuery
from app.domain.users.core.schemas import UserDetails


class CurrentUserTokenQuery:
    def __init__(self, token_ctx_var: ContextVar) -> None:
        self.token_ctx_var = token_ctx_var

    async def __call__(self) -> str | None:
        return self.token_ctx_var.get()


class TokenPayloadQuery:
    def __init__(self, jwt_service: tokens.JwtServiceBase) -> None:
        self.jwt_service = jwt_service

    async def __call__(self, token: str, validate: bool = True) -> schemas.TokenPayload:
        print("Received token:", token)
        with self._handle_auth_exceptions():
            decoded_token = await self.jwt_service.decode(token, validate)

        return schemas.TokenPayload.model_validate(decoded_token)

    @contextmanager
    def _handle_auth_exceptions(self):
        try:
            yield
        except tokens.ExpiredSignatureError:
            raise AuthError(code=enums.AuthErrorCodes.expired_signature, message="Signature has expired")
        except tokens.InvalidSignatureError:
            raise AuthError(code=enums.AuthErrorCodes.invalid_signature, message="Signature verification failed")


class CurrentUserTokenPayloadQuery:
    def __init__(
            self,
            token_query: CurrentUserTokenQuery,
            token_payload_query: TokenPayloadQuery,
    ) -> None:
        self.token_query = token_query
        self.token_payload_query = token_payload_query

    async def __call__(self) -> schemas.TokenPayload | None:
        token = await self.token_query()
        if not token:
            return None

        return await self.token_payload_query(token)


class CurrentUserQuery:
    def __init__(self, token_query: CurrentUserTokenPayloadQuery, user_query: UserRetrieveQuery) -> None:
        self.token_query = token_query
        self.user_query = user_query

    async def __call__(self) -> UserDetails:
        token_payload = await self.token_query()
        if token_payload:
            user = await self.user_query(token_payload.sub)

            return UserDetails.model_validate(user)
        raise AuthError(code=enums.AuthErrorCodes.invalid_token)
