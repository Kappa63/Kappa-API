from datetime import datetime, timezone
from ._base import Base
import sqlalchemy as sa
import uuid
import enum

class Permissions(enum.IntFlag):
    GENERAL = 1
    PRIVATE = 2
    ADMIN = 4

class User(Base):
    __tablename__ = "users"

    apiKey = sa.Column(sa.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = sa.Column(sa.String, nullable=False, unique=True)
    passwordHash = sa.Column(sa.String, nullable=False)
    perms = sa.Column(sa.Integer, nullable=False, default=Permissions.GENERAL)
    isActive = sa.Column(sa.Boolean, default=True)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    lastUse = sa.Column(sa.DateTime)