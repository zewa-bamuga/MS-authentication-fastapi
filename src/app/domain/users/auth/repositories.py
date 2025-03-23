import uuid

from a8t_tools.db.transactions import AsyncDbTransaction
from sqlalchemy import delete, insert, select

from app.domain.common import models
from app.domain.users.auth import schemas


class TokenRepository:
    def __init__(self, transaction: AsyncDbTransaction):
        self.transaction = transaction

    async def create_token_info(self, payload: schemas.TokenInfo) -> None:
        stmt = insert(models.Token).values(
            {
                "user_id": payload.user_id,
                "refresh_token_id": payload.token_id,
            },
        )
        async with self.transaction.use() as session:
            await session.execute(stmt)

    async def get_token_info(self, token_id: uuid.UUID) -> schemas.TokenInfo | None:
        stmt = select(models.Token).where(models.Token.refresh_token_id == token_id)

        async with self.transaction.use() as session:
            result = (await session.execute(stmt)).scalar_one_or_none()

        if result is None:
            return None

        return schemas.TokenInfo(
            user_id=result.user_id, token_id=result.refresh_token_id
        )

    async def delete_tokens(self, token_id: uuid.UUID) -> None:
        stmt = delete(models.Token).where(models.Token.refresh_token_id == token_id)

        async with self.transaction.use() as session:
            await session.execute(stmt)
