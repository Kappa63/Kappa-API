from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa


class ScheduleDoses(Base):
    __tablename__ = DoseGuardConfig.SQL_SCHEDULE_DOSES_TABLE


    scheduleId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_SCHEDULE_TABLE + ".id"), primary_key=True)
    doseId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_DOSES_TABLE + ".id"), primary_key=True)


    def toDict(self):
        return {
            "scheduleId": self.scheduleId,
            "doseId": self.doseId
        }