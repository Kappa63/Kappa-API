from datetime import datetime, timezone
from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa


class Schedule(Base):
    __tablename__ = DoseGuardConfig.SQL_SCHEDULE_TABLE

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    active = sa.Column(sa.Boolean, default=True)

    
    patients = sa.orm.relationship("Patient", secondary=DoseGuardConfig.SQL_PATIENT_SCHEDULE_TABLE, back_populates="schedules")
    doses = sa.orm.relationship("Dose", secondary=DoseGuardConfig.SQL_SCHEDULE_DOSES_TABLE, back_populates="schedules")


    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
        }