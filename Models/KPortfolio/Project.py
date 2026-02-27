from datetime import datetime, timezone
from Config import KPortfolioConfig
from ..BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa

class Project(BaseAuditEntity):
    __tablename__ = KPortfolioConfig.SQL_PORTFOLIO_PROJECTS_TABLE

    imageURL = sa.Column(sa.String, nullable=False, unique=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    link = sa.Column(sa.String, nullable=True)

    def toDict(self):
        return {
            "id": self.id,
            "imageURL": self.imageURL,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn
        }

class DetachedProject:
    def __init__(self, project: Project) -> None:
        self.imageURL = project.imageURL
        self.title = project.title
        self.description = project.description
        self.link = project.link