import enum


class ErrorCodes(enum.StrEnum):
    api_error = enum.auto()
    not_found = enum.auto()
    auth_error = enum.auto()
    permission_error = enum.auto()
    database_error = enum.auto()


class AuthErrorCodes(enum.StrEnum):
    invalid_credentials = enum.auto()
    invalid_signature = enum.auto()
    invalid_token = enum.auto()
    expired_signature = enum.auto()


class UserStatuses(enum.StrEnum):
    unconfirmed = enum.auto()
    active = enum.auto()
    banned = enum.auto()


class TaskNames(enum.StrEnum):
    activate_user = enum.auto()


class TaskQueues(enum.StrEnum):
    main_queue = enum.auto()
