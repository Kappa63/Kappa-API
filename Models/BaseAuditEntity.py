from datetime import datetime, timezone
from Config import DoseGuardConfig
import sqlalchemy as sa
from ._base import Base

class BaseAuditEntity(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    createdBy = sa.Column(sa.Integer, sa.ForeignKey(DoseGuardConfig.SQL_CAREGIVER_TABLE + ".id"), nullable=True)
    active = sa.Column(sa.Boolean, default=True)

