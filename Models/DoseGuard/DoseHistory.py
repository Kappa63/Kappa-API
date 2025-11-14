from datetime import datetime, timezone
from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa


class DoseHistory(Base):
    __tablename__ = DoseGuardConfig.SQL_DOSE_HISTORY_TABLE

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    patientId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_PATIENT_TABLE + ".id"), nullable=False)
    doseId = sa.Column(sa.BigInteger, sa.ForeignKey(DoseGuardConfig.SQL_DOSES_TABLE + ".id"), nullable=False)
    taken = sa.Column(sa.Boolean, nullable=False, default=False)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    active = sa.Column(sa.Boolean, default=True)

    patient = sa.orm.relationship("Patient", back_populates="doseHistory")
    dose = sa.orm.relationship("Dose", back_populates="history")
