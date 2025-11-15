from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa


class CaregiverPatient(Base):
    __tablename__ = DoseGuardConfig.SQL_CAREGIVER_PATIENT_TABLE


    caregiverId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_CAREGIVER_TABLE + ".id"), primary_key=True)
    patientId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_PATIENT_TABLE + ".id"), primary_key=True)


    def toDict(self):
        return {
            "caregiverId": self.caregiverId,
            "patientId": self.patientId
        }