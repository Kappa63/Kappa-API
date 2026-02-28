from datetime import datetime, timezone
from Config import DoseGuardConfig
from Config import DoseGuardConfig
from Models.BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa


class Pill(BaseAuditEntity):
    __tablename__ = DoseGuardConfig.SQL_PILLS_TABLE

    name = sa.Column(sa.String(50), nullable=False)
    strength = sa.Column(sa.Float, nullable=False)


    doses = sa.orm.relationship("Dose", back_populates="pill")


    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "strength": self.strength,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn,
            "createdBy": self.createdBy,
        }