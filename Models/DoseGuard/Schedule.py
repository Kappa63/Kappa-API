from datetime import datetime, timezone
from Config import DoseGuardConfig
from Config import DoseGuardConfig
from Models.BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa


class Schedule(BaseAuditEntity):
    __tablename__ = DoseGuardConfig.SQL_SCHEDULE_TABLE

    name = sa.Column(sa.String(50), nullable=False)

    
    patients = sa.orm.relationship("Patient", secondary=DoseGuardConfig.SQL_PATIENT_SCHEDULE_TABLE, back_populates="schedules")
    doses = sa.orm.relationship("Dose", secondary=DoseGuardConfig.SQL_SCHEDULE_DOSES_TABLE, back_populates="schedules")


    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
            "createdBy": self.createdBy,
        }