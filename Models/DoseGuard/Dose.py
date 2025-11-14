from datetime import datetime, timezone
from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa


class Dose(Base):
    __tablename__ = DoseGuardConfig.SQL_DOSES_TABLE

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    pillId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_PILLS_TABLE + ".id"), nullable=False)
    interval = sa.Column(sa.BigInteger, nullable=False)
    amount = sa.Column(sa.BigInteger, nullable=False)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    active = sa.Column(sa.Boolean, default=True)

    pill = sa.orm.relationship("Pill", back_populates="doses")
    schedules = sa.orm.relationship("Schedule", secondary=DoseGuardConfig.SQL_SCHEDULE_DOSES_TABLE, back_populates="doses")
    history = sa.orm.relationship("DoseHistory", back_populates="dose")
