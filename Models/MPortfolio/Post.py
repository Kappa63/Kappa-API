from datetime import datetime, timezone
from Config import MPortfolioConfig
from .._base import Base
import sqlalchemy as sa

class Post(Base):
    __tablename__ = MPortfolioConfig.SQL_PORTFOLIO_POSTS_TABLE

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    imageURL = sa.Column(sa.String, nullable=False, unique=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    category = sa.Column(sa.String, nullable=False)
    state = sa.Column(sa.Boolean, nullable=False, default=True)

    createdOn = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedOn = sa.Column(sa.DateTime, onupdate=lambda: datetime.now(timezone.utc))

class DetachedPost:
    def __init__(self, post: Post) -> None:
        self.imageURL = post.imageURL
        self.title = post.title
        self.description = post.description
        self.category = post.category