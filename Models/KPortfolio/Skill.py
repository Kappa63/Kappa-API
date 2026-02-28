from datetime import datetime, timezone
from Config import KPortfolioConfig
from ..BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa

class Skill(BaseAuditEntity):
    __tablename__ = KPortfolioConfig.SQL_PORTFOLIO_SKILLS_TABLE

    category = sa.Column(sa.String, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    icon = sa.Column(sa.String, nullable=True)
    order = sa.Column(sa.Integer, nullable=False)

    def toDict(self):
        return {
            "id": self.id,
            "category": self.category,
            "name": self.name,
            "icon": self.icon,
            "order": self.order,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn
        }

class DetachedSkill:
    def __init__(self, skill: Skill) -> None:
        self.category = skill.category
        self.name = skill.name
        self.icon = skill.icon
        self.order = skill.order