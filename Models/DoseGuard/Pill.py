from datetime import datetime, timezone
from Config import DoseGuardConfig
from Models._base import Base
import sqlalchemy as sa


class Pill(Base):
    __tablename__ = DoseGuardConfig.SQL_PILLS_TABLE

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    strength = sa.Column(sa.Float, nullable=False)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    active = sa.Column(sa.Boolean, default=True)


    doses = sa.orm.relationship("Dose", back_populates="pill")


    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "strength": self.strength,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
        }