from uuid import UUID

from a8t_tools.db.pagination import NoPaginationResults, Paginated, PaginationCallable
from a8t_tools.db.sorting import SortingData, apply_sorting
from a8t_tools.db.transactions import AsyncDbTransaction
from sqlalchemy import insert, select

from app.domain.common import models
from app.domain.common.schemas import IdContainer
from app.domain.storage.attachments import schemas


class AttachmentRepository:
    def __init__(self, transaction: AsyncDbTransaction):
        self.transaction = transaction

    async def get_attachments(
        self,
        pagination: PaginationCallable[schemas.Attachment] | None = None,
        sorting: SortingData[schemas.AttachmentSorts] | None = None,
    ) -> Paginated[schemas.Attachment]:
        query = apply_sorting(select(models.Attachment), sorting)

        async with self.transaction.use() as db:
            if pagination is None:
                results = (await db.execute(query)).scalars().all()
                return NoPaginationResults(
                    [schemas.Attachment.model_validate(x) for x in results]
                )

            return await pagination(db, query)

    async def get_attachment_or_none(
        self, attachment_id: UUID
    ) -> schemas.Attachment | None:
        query = select(models.Attachment).where(models.Attachment.id == attachment_id)

        async with self.transaction.use() as db:
            result = (await db.execute(query)).scalar_one_or_none()
            if not result:
                return None
            return schemas.Attachment.model_validate(result)

    async def create_attachment(
        self, payload: schemas.AttachmentCreateFull
    ) -> IdContainer:
        query = (
            insert(models.Attachment)
            .values(**payload.model_dump())
            .returning(models.Attachment.id)
        )

        async with self.transaction.use() as db:
            id_ = (await db.execute(query)).scalar_one()
            return IdContainer(id=id_)
