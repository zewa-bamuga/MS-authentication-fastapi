import asyncio
import functools
from collections.abc import Callable
from typing import Any

import typer
from a8t_tools.db.exceptions import DatabaseError
from loguru import logger

import app.domain
from app.containers import Container
from app.domain.users.core.schemas import UserCreate
from app.domain.users.permissions.schemas import BasePermissions


def async_to_sync(fn: Callable[..., Any]) -> Callable[..., Any]:
    if not asyncio.iscoroutinefunction(fn):
        return fn

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        coro = fn(*args, **kwargs)
        return asyncio.get_event_loop().run_until_complete(coro)

    return wrapper


def create_container() -> Container:
    container = Container()
    container.wire(packages=[app.domain])
    container.init_resources()
    return container


container = create_container()
typer_app = typer.Typer()


@typer_app.command()
@async_to_sync
async def noop() -> None:
    pass


@typer_app.command()
@async_to_sync
async def create_superuser(
    firstname: str = typer.Argument(...),
    lastname: str = typer.Argument(...),
    email: str = typer.Argument(...),
    password: str = typer.Argument(...),
) -> None:
    password_hash = await container.user.password_hash_service().hash(password)
    command = container.user.create_command()
    try:
        await command(
            UserCreate(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password_hash=password_hash,
                permissions={BasePermissions.superuser},
            ),
        )
    except DatabaseError as err:
        logger.warning(f"Superuser creation error: {err}")
