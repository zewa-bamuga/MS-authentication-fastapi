import re
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from typing import IO

from a8t_tools.storage.facade import FileStorage

from app.domain.storage.attachments import schemas
from app.domain.storage.attachments.repositories import AttachmentRepository


class AttachmentCreateCommand:
    def __init__(
            self,
            repository: AttachmentRepository,
            file_storage: FileStorage,
            bucket: str,
            max_name_len: int = 60,
    ):
        self.repository = repository
        self.file_storage = file_storage
        self.bucket = bucket
        self.max_name_len = max_name_len

    async def __call__(self, payload: schemas.AttachmentCreate) -> schemas.Attachment:
        name = payload.name or self._get_random_name()
        path = self._generate_path(name)
        uri = await self.file_storage.upload_file(self.bucket, path, payload.file)
        id_container = await self.repository.create_attachment(
            schemas.AttachmentCreateFull(
                name=name,
                path=path,
                uri=uri,
            )
        )
        attachment = await self.repository.get_attachment_or_none(id_container.id)
        assert attachment
        return attachment

    def _generate_path(self, name: str) -> str:
        now = datetime.now()
        folder = now.strftime("%Y/%m/%d")
        timestamp = now.strftime("%s")
        stripped_slugified_name = self._slugify(name)[: self.max_name_len]
        return f"/{folder}/{timestamp}.{stripped_slugified_name}"

    @classmethod
    def _get_random_name(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def _slugify(cls, s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"[^\w\s\.-]", "", s)
        s = re.sub(r"[\s_-]+", "-", s)
        s = re.sub(r"^-+|-+$", "", s)
        return s


class AttachmentDataRetrieveCommand:
    def __init__(
            self,
            file_storage: FileStorage,
            bucket: str,
    ):
        self.file_storage = file_storage
        self.bucket = bucket

    @asynccontextmanager
    async def __call__(self, attachment: schemas.Attachment) -> AsyncIterator[IO[bytes]]:
        async with self.file_storage.receive_file(self.bucket, attachment.path) as file:
            yield file
