from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy import create_engine
from Models._base import Base

engine = create_engine('sqlite:///SerApi.db', echo=False)
Session = sessionmaker(bind=engine)

def initDB():
    Base.metadata.create_all(engine)

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