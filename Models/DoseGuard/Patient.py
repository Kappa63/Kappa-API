from datetime import datetime, timezone
from Config import DoseGuardConfig
from Config import DoseGuardConfig
from Models.BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa


class Patient(BaseAuditEntity):
    __tablename__ = DoseGuardConfig.SQL_PATIENT_TABLE

    name = sa.Column(sa.String(50), nullable=False)
    contact = sa.Column(sa.String(25))
    age = sa.Column(sa.Integer)
    weight = sa.Column(sa.Float)
    height = sa.Column(sa.Float)


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