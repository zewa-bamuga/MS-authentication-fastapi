from uuid import UUID

from app.domain.common.schemas import APIModel


class TokenResponse(APIModel):
    access_token: str
    token_type: str = "Bearer"
    refresh_token: str


class TokenPayload(APIModel):
    sub: UUID


class TokenInfo(APIModel):
    user_id: UUID | None = None
    token_id: UUID
