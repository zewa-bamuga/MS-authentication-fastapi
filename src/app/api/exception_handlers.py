import functools
from typing import Any, Callable, Coroutine

from fastapi import Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.api.schemas import AuthApiError, SimpleApiError
from app.domain.common import enums, exceptions


async def universal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    response_content = SimpleApiError(
        code=enums.ErrorCodes.api_error, message="Unknown error"
    ).model_dump()
    return JSONResponse(
        status_code=500,
        content=response_content,
    )


def typed_exception_handler(
    exc_type: type[BaseModel],
) -> Callable[[Request, exceptions.GenericApiError], Coroutine[Any, Any, JSONResponse]]:
    async def exception_handler(
        _: Request, exc: exceptions.GenericApiError
    ) -> JSONResponse:
        response_content = exc_type.model_validate(exc).model_dump()
        partial_resp = functools.partial(
            JSONResponse, status_code=exc.status_code, content=response_content
        )
        if exc.headers:
            return partial_resp(exc.headers)
        return partial_resp()

    return exception_handler


registry = [
    (exceptions.GenericApiError, typed_exception_handler(SimpleApiError)),
    (exceptions.AuthError, typed_exception_handler(AuthApiError)),
    (Exception, universal_exception_handler),
]
