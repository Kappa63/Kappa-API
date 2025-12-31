from datetime import datetime, timezone
from Config import DoseGuardConfig
from Config import DoseGuardConfig
from Models.BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa


class Dose(BaseAuditEntity):
    __tablename__ = DoseGuardConfig.SQL_DOSES_TABLE

    pillId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_PILLS_TABLE + ".id"), nullable=False)
    interval = sa.Column(sa.BigInteger, nullable=False)
    amount = sa.Column(sa.BigInteger, nullable=False)


    pill = sa.orm.relationship("Pill", back_populates="doses")
    schedules = sa.orm.relationship("Schedule", secondary=DoseGuardConfig.SQL_SCHEDULE_DOSES_TABLE, back_populates="doses")
    history = sa.orm.relationship("DoseHistory", back_populates="dose")


    def toDict(self):
        return {
            "id": self.id,
            "pillId": self.pillId,
            "interval": self.interval,
            "amount": self.amount,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
        }