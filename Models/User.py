from datetime import datetime, timezone
from Utils.Enums import Permissions
from Config import EnvConfig
from .BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa
import uuid

class User(BaseAuditEntity):
    __tablename__ = EnvConfig.SQL_USERS_TABLE

    apiKey = sa.Column(sa.String, unique=True, default=lambda: str(uuid.uuid4()))
    username = sa.Column(sa.String, nullable=False, unique=True)
    passwordHash = sa.Column(sa.String, nullable=False)
    perms = sa.Column(sa.Integer, nullable=False, default=Permissions.GENERAL)

    lastUse = sa.Column(sa.DateTime)

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "perms": self.perms,
            "apiKey": self.apiKey
        }
    
    caregiverProfile = sa.orm.relationship("Caregiver", uselist=False, back_populates="user", foreign_keys="Caregiver.userId")

class DetachedUser:
    def __init__(self, user: User) -> None:
        self.id = user.id
        self.username = user.username
        self.perms = user.perms