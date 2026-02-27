from datetime import datetime, timezone
from Config import MPortfolioConfig
from ..BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa

class Post(BaseAuditEntity):
    __tablename__ = MPortfolioConfig.SQL_PORTFOLIO_POSTS_TABLE

    imageURL = sa.Column(sa.String, nullable=False, unique=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    category = sa.Column(sa.String, nullable=False)
    order = sa.Column(sa.Integer, nullable=False, default=0)

    def toDict(self):
        return {
            "id": self.id,
            "imageURL": self.imageURL,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "order": self.order,
            "active": self.active,
            "createdOn": self.createdOn,
            "updatedOn": self.updatedOn
        }

class DetachedPost:
    def __init__(self, post: Post) -> None:
        self.imageURL = post.imageURL
        self.title = post.title
        self.description = post.description
        self.category = post.category