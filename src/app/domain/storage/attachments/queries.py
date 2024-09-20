from uuid import UUID

from a8t_tools.db.pagination import Paginated

from app.domain.common.exceptions import NotFoundError
from app.domain.storage.attachments import schemas
from app.domain.storage.attachments.repositories import AttachmentRepository


class AttachmentListQuery:
    def __init__(self, repository: AttachmentRepository):
        self.repository = repository

    async def __call__(self, payload: schemas.AttachmentListRequestSchema) -> Paginated[schemas.Attachment]:
        return await self.repository.get_attachments(payload.pagination, payload.sorting)


class AttachmentRetrieveQuery:
    def __init__(self, repository: AttachmentRepository):
        self.repository = repository

    async def __call__(self, attachment_id: UUID) -> schemas.Attachment:
        result = await self.repository.get_attachment_or_none(attachment_id)
        if not result:
            raise NotFoundError()
        return result
