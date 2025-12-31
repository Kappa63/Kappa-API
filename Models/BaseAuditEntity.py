from datetime import datetime, timezone
import sqlalchemy as sa
from ._base import Base

class BaseAuditEntity(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    active = sa.Column(sa.Boolean, default=True)
