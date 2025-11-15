from datetime import datetime, timezone
from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa
import uuid


class Caregiver(Base):
    __tablename__ = DoseGuardConfig.SQL_CAREGIVER_TABLE

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    username = sa.Column(sa.String(50), nullable=False, unique=True)
    passwordHash = sa.Column(sa.String(100), nullable=False)
    apiKey = sa.Column(sa.String, unique=True, default=lambda: str(uuid.uuid4()))

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    active = sa.Column(sa.Boolean, default=True)


    patients = sa.orm.relationship("Patient", secondary=DoseGuardConfig.SQL_CAREGIVER_PATIENT_TABLE, back_populates="caregivers")
    

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
        }