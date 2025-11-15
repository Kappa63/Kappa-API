from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa


class PatientSchedule(Base):
    __tablename__ = DoseGuardConfig.SQL_PATIENT_SCHEDULE_TABLE


    patientId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_PATIENT_TABLE + ".id"), primary_key=True)
    scheduleId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_SCHEDULE_TABLE + ".id"), primary_key=True)


    def toDict(self):
        return {
            "patientId": self.patientId,
            "scheduleId": self.scheduleId
        }