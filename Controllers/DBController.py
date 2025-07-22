from sqlalchemy.orm import sessionmaker
from Functions.Helpers import hashPass
from contextlib import contextmanager
from sqlalchemy import create_engine
from Models import User, Permissions
from Models._base import Base
from config import Config

engine = create_engine(f"sqlite:///{Config.SQL_DB}.db", echo=False)
Session = sessionmaker(bind=engine)

def initDB():
    Base.metadata.create_all(engine)
    setupAdminUser()

@contextmanager
def getSession():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def setupAdminUser():
    with getSession() as session:
        if not session.query(User).filter_by(username=Config.ADMIN_USERNAME).first():
            session.add(User(
                            username=Config.ADMIN_USERNAME,
                            passwordHash=hashPass(Config.ADMIN_PASSWORD),
                            perms=Permissions.GENERAL|Permissions.PRIVATE|Permissions.ADMIN
                        ))