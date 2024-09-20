from dependency_injector import containers, providers

from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.storage.facade import FileStorage

from app.domain.storage.attachments.commands import AttachmentCreateCommand
from app.domain.storage.attachments.queries import (
    AttachmentListQuery,
    AttachmentRetrieveQuery,
)
from app.domain.storage.attachments.repositories import AttachmentRepository


class AttachmentContainer(containers.DeclarativeContainer):
    transaction = providers.Dependency(instance_of=AsyncDbTransaction)

    file_storage = providers.Dependency(instance_of=FileStorage)

    bucket = providers.Dependency(instance_of=str)

    repository = providers.Factory(AttachmentRepository, transaction=transaction)

    list_query = providers.Factory(AttachmentListQuery, repository=repository)

    retrieve_query = providers.Factory(AttachmentRetrieveQuery, repository=repository)

    create_command = providers.Factory(
        AttachmentCreateCommand,
        repository=repository,
        file_storage=file_storage,
        bucket=bucket,
    )
