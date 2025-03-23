from typing import Any

from app.domain.common import enums
from app.domain.common.enums import ErrorCodes


class GenericApiError(Exception):
    code: ErrorCodes = ErrorCodes.api_error
    message: str = "Generic Error"
    status_code: int = 500
    headers: dict[str, str] | None = None

    def __init__(
        self,
        code: ErrorCodes | None = None,
        message: str | None = None,
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
        *args: Any,
    ) -> None:
        if code is not None:
            self.code = code
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        if headers is not None:
            self.headers = headers
        super().__init__(message, *args)


class NotFoundError(GenericApiError):
    code: ErrorCodes = ErrorCodes.not_found
    message: str = "Object not found"
    status_code: int = 404


class AuthError(GenericApiError):
    code: ErrorCodes = ErrorCodes.auth_error
    message: str = "Invalid credentials"
    status_code: int = 401

    def __init__(
        self,
        code: enums.AuthErrorCodes,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.payload = {
            "code": code,
        }
        super().__init__(*args, **kwargs)


class UserPermissionError(GenericApiError):
    code: ErrorCodes = ErrorCodes.permission_error
    message: str = "Permission Error"
    status_code: int = 403
