from datetime import datetime, timezone
from Config import DoseGuardConfig
from Config import DoseGuardConfig
from Models.BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa


class DoseHistory(BaseAuditEntity):
    __tablename__ = DoseGuardConfig.SQL_DOSE_HISTORY_TABLE

    patientId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_PATIENT_TABLE + ".id"), nullable=False)
    doseId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_DOSES_TABLE + ".id"), nullable=False)
    taken = sa.Column(sa.Boolean, nullable=False, default=False)


    patient = sa.orm.relationship("Patient", back_populates="doseHistory")
    dose = sa.orm.relationship("Dose", back_populates="history")


    def toDict(self):
        return {
            "id": self.id,
            "patientId": self.patientId,
            "doseId": self.doseId,
            "taken": self.taken,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
            "createdBy": self.createdBy,
        }