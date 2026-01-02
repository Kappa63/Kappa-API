from datetime import datetime, timezone
from Config import DoseGuardConfig
from Config import DoseGuardConfig
from Models.BaseAuditEntity import BaseAuditEntity
from Config import EnvConfig
import sqlalchemy as sa

class Caregiver(BaseAuditEntity):
    __tablename__ = DoseGuardConfig.SQL_CAREGIVER_TABLE

    userId = sa.Column(sa.Integer, sa.ForeignKey(EnvConfig.SQL_USERS_TABLE + ".id"), unique=True, nullable=False)

    name = sa.Column(sa.String(50), nullable=False)

    user = sa.orm.relationship("User", foreign_keys=[userId], back_populates="caregiverProfile")
    patients = sa.orm.relationship("Patient", secondary=DoseGuardConfig.SQL_CAREGIVER_PATIENT_TABLE, back_populates="caregivers")

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user": self.user.toDict() if self.user else None,
            "active": self.active,
            "createdOn": self.createdOn,
        }