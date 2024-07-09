from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL = 'sqlite:///./team.db'

engine= create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

Base= declarative_base()

metadata = MetaData()
metadata.reflect(bind=engine)

def get_db(): #get a db session
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
