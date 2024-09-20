from typing import Any

from dependency_injector import wiring

from app.containers import Container
from app.domain.common.enums import TaskNames
from app.domain.common.schemas import IdContainer
from app.domain.users.core.commands import UserActivateCommand
from a8t_tools.bus.consumer import consume


@consume(TaskNames.activate_user)
@wiring.inject
async def activate_user(
        user_id_container_dict: dict[str, Any],
        activate_user: UserActivateCommand = wiring.Provide[Container.user.activate_command],
) -> None:
    user_id_container = IdContainer.model_validate(user_id_container_dict)
    await activate_user(user_id_container.id)
