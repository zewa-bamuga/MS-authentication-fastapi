import enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr
from pydantic import EmailStr

from app.domain.common.enums import UserStatuses
from app.domain.common.schemas import APIModel
from app.domain.storage.attachments.schemas import Attachment
from app.domain.users.permissions.schemas import BasePermissions


class User(APIModel):
    id: UUID
    firstname: str
    lastname: str
    middle_name: str | None = None
    phone: str | None = None
    email: EmailStr
    description: str | None = None
    status: UserStatuses
    avatar_attachment_id: UUID | None = None
    created_at: datetime
    is_subscribed: bool = False


class UserDetails(User):
    avatar_attachment: Attachment | None = None


class UserDetailsFull(UserDetails):
    permissions: set[str] | None = None


class UserCredentials(APIModel):
    email: str
    password: str


class UsersByIdsRequest(APIModel):
    ids: list[UUID]


class UserCredentialsRegist(APIModel):
    firstname: str
    lastname: str
    middle_name: str
    phone: str
    email: str
    permissions: set[str] | None = None
    password: str


class UserCreate(APIModel):
    firstname: str | None = None
    lastname: str | None = None
    middle_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    password_hash: str
    avatar_attachment_id: UUID | None = None
    permissions: set[str] | None = None
    is_subscribed: bool = False


class UserCreateFull(UserCreate):
    status: UserStatuses


class UserPartialUpdate(APIModel):
    firstname: str | None = None
    email: EmailStr | None = None
    avatar_attachment_id: UUID | None = None
    password_hash: str | None = None
    permissions: set[str] | None = None
    status: str | None = None
    is_subscribed: bool = False


class UserPasswordUpdate(APIModel):
    old_password: str
    new_password: str


class UserPartialUpdateFull(APIModel):
    password_hash: str | None = None


class UserInternal(APIModel):
    id: UUID
    firstname: str
    lastname: str
    middle_name: str | None = None
    phone: str | None = None
    email: EmailStr
    description: str | None = None
    password_hash: str
    permissions: set[str] | None = None
    avatar_attachment_id: UUID | None = None
    status: UserStatuses
    created_at: datetime
    is_subscribed: bool = False


class UserSorts(enum.StrEnum):
    id = enum.auto()
    firstname = enum.auto()
    email = enum.auto()
    permissions = enum.auto()
    status = enum.auto()
    created_at = enum.auto()


class EmailForCode(APIModel):
    email: str | None = None


class VerificationCode(APIModel):
    code: int


class UpdatePasswordConfirm(APIModel):
    email: str | None = None
    code: str | None = None
    password: str | None = None


class UserProfilePartialUpdate(APIModel):
    firstname: str | None = None
    password: str | None = None


class PasswordResetCode(APIModel):
    user_id: UUID | None = None
    code: str


class EmailVerificationCode(APIModel):
    email: str
    code: int


class PasswordResetCodePartialUpdate(APIModel):
    code: str | None = None


@dataclass
class UserWhere:
    id: UUID | None = None
    firstname: str | None = None
    permissions: str | None = "student"
    email: str | None = None


@dataclass
class UserListRequestSchema:
    pagination: pg.PaginationCallable[User] | None = None
    sorting: sr.SortingData[UserSorts] | None = None
    where: UserWhere | None = None


@dataclass
class PasswordResetCodeWhere:
    id: int | None = None
    user_id: UUID | None = None
    code: str | None = None
