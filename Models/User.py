from datetime import datetime, timezone
from config import Config
from ._base import Base
import sqlalchemy as sa
import uuid
import enum

class Permissions(enum.IntFlag):
    DEFAULT = 0
    GENERAL = 1
    PRIVATE = 2
    ADMIN = 4

class User(Base):
    __tablename__ = Config.SQL_USERS_TABLE

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    apiKey = sa.Column(sa.String, unique=True, default=lambda: str(uuid.uuid4()))
    username = sa.Column(sa.String, nullable=False, unique=True)
    passwordHash = sa.Column(sa.String, nullable=False)
    perms = sa.Column(sa.Integer, nullable=False, default=Permissions.GENERAL)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    lastUse = sa.Column(sa.DateTime)

class DetachedUser:
    def __init__(self, user: User) -> None:
        self.id = user.id
        self.username = user.username
        self.perms = user.perms