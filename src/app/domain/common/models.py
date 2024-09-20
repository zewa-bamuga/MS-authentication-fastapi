import datetime
import secrets
import uuid
import random

import sqlalchemy as sa
from sqlalchemy import orm, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


@orm.as_declarative()
class Base:
    __tablename__: str

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Attachment(Base):
    __tablename__ = "attachment"

    name: orm.Mapped[str]
    path: orm.Mapped[str]
    uri: orm.Mapped[str | None]


class User(Base):
    __tablename__ = "user"

    firstname = Column(String, unique=False, nullable=True)
    lastname = Column(String, unique=False, nullable=True)
    email = Column(String, unique=True, nullable=True)
    description = Column(String, unique=False, nullable=True)
    status = Column(String)
    password_hash = Column(String)
    avatar_attachment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attachment.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    permissions: orm.Mapped[set[str] | None] = orm.mapped_column(ARRAY(sa.String))

    avatar_attachment = relationship(
        "Attachment",
        backref="user_avatar_attachment",
        foreign_keys=[avatar_attachment_id],
        uselist=False,
    )
    token = relationship("Token", back_populates="user")
    password_reset_code = relationship("PasswordResetCode", back_populates="user")


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=True)
    refresh_token_id = Column(UUID(as_uuid=True))

    user = relationship("User", back_populates="token")


class PasswordResetCode(Base):
    __tablename__ = "password_reset_code"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=True)
    code = Column(String, nullable=False)

    user_id_user_fk = ForeignKey('user.id')

    user = relationship("User", back_populates="password_reset_code")

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(6)


class EmailCode(Base):
    __tablename__ = 'email_code'

    id = Column(Integer, primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    code: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False)

    @classmethod
    def generate_code(cls) -> int:
        return random.randint(1000, 9999)
