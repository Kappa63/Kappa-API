from datetime import datetime, timezone
from Config import MPortfolioConfig
from Config import MPortfolioConfig
from ..BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa

class Post(BaseAuditEntity):
    __tablename__ = MPortfolioConfig.SQL_PORTFOLIO_POSTS_TABLE

    imageURL = sa.Column(sa.String, nullable=False, unique=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    category = sa.Column(sa.String, nullable=False)
    # state was renamed to active in BaseAuditEntity

class DetachedPost:
    def __init__(self, post: Post) -> None:
        self.imageURL = post.imageURL
        self.title = post.title
        self.description = post.description
        self.category = post.category