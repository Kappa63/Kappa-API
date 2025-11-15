from datetime import datetime, timezone
from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa


class Patient(Base):
    __tablename__ = DoseGuardConfig.SQL_PATIENT_TABLE

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    contact = sa.Column(sa.String(25))
    age = sa.Column(sa.Integer)
    weight = sa.Column(sa.Float)
    height = sa.Column(sa.Float)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    active = sa.Column(sa.Boolean, default=True)


    caregivers = sa.orm.relationship("Caregiver", secondary=DoseGuardConfig.SQL_CAREGIVER_PATIENT_TABLE, back_populates="patients")
    schedules = sa.orm.relationship("Schedule", secondary=DoseGuardConfig.SQL_PATIENT_SCHEDULE_TABLE, back_populates="patients")
    doseHistory = sa.orm.relationship("DoseHistory", back_populates="patient")


    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact": self.contact,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
        }