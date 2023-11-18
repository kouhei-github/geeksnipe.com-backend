from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

port = os.environ["PORT"]
user = os.environ["USERNAME"]
password = os.environ["USERPASS"]
database = os.environ["DATABASE"]
host = os.environ["HOST"]

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
