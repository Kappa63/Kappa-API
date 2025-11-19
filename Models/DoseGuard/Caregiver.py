from datetime import datetime, timezone
from Config import DoseGuardConfig
from Models._base import Base
from Config import EnvConfig
import sqlalchemy as sa

class Caregiver(Base):
    __tablename__ = DoseGuardConfig.SQL_CAREGIVER_TABLE

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    userId = sa.Column(sa.Integer, sa.ForeignKey(EnvConfig.SQL_USERS_TABLE + ".id"), unique=True, nullable=False)

    name = sa.Column(sa.String(50), nullable=False)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    active = sa.Column(sa.Boolean, default=True)

    user = sa.orm.relationship("User", back_populates="caregiverProfile")
    patients = sa.orm.relationship("Patient", secondary=DoseGuardConfig.SQL_CAREGIVER_PATIENT_TABLE, back_populates="caregivers")

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user": self.user.toDict() if self.user else None,
            "active": self.active,
            "createdOn": self.createdOn,
        }