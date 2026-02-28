from Config import MPortfolioConfig
from ..BaseAuditEntity import BaseAuditEntity
import sqlalchemy as sa

class General(BaseAuditEntity):
    __tablename__ = MPortfolioConfig.SQL_PORTFOLIO_GENERAL_TABLE

    key = sa.Column(sa.String, nullable=False, unique=True)
    value = sa.Column(sa.String, nullable=False)

class DetachedGeneral:
    def __init__(self, item: General) -> None:
        self.key = item.key
        self.value = item.value
