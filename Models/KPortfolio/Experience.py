from datetime import datetime, timezone
from Config import KPortfolioConfig
from ..BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa

class Experience(BaseAuditEntity):
    __tablename__ = KPortfolioConfig.SQL_PORTFOLIO_EXPERIENCES_TABLE

    role = sa.Column(sa.String, nullable=False)
    company = sa.Column(sa.String, nullable=False)
    startDate = sa.Column(sa.Date, nullable=False)
    endDate = sa.Column(sa.Date, nullable=True)
    highlights = sa.Column(sa.String, nullable=False)
    # order = sa.Column(sa.Integer, nullable=False)

    def toDict(self):
        return {
            "id": self.id,
            "role": self.role,
            "company": self.company,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "highlights": self.highlights,
            # "order": self.order,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn
        }

class DetachedExperience:
    def __init__(self, experience: Experience) -> None:
        self.role = experience.role
        self.company = experience.company
        self.startDate = experience.startDate
        self.endDate = experience.endDate
        self.highlights = experience.highlights
        # self.order = experience.order