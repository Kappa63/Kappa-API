from datetime import datetime, timezone
from Utils.Enums import Permissions
from Config import EnvConfig
from ._base import Base
import sqlalchemy as sa
import uuid

class User(Base):
    __tablename__ = EnvConfig.SQL_USERS_TABLE

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    apiKey = sa.Column(sa.String, unique=True, default=lambda: str(uuid.uuid4()))
    username = sa.Column(sa.String, nullable=False, unique=True)
    passwordHash = sa.Column(sa.String, nullable=False)
    perms = sa.Column(sa.Integer, nullable=False, default=Permissions.GENERAL)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    lastUse = sa.Column(sa.DateTime)

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "perms": self.perms,
        }
    
    caregiverProfile = sa.orm.relationship("Caregiver", uselist=False, back_populates="user")

class DetachedUser:
    def __init__(self, user: User) -> None:
        self.id = user.id
        self.username = user.username
        self.perms = user.perms