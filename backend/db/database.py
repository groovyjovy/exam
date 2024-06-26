from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE = "mysql+pymysql"
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASS']
HOST = os.environ['DB_HOST']
PORT = "3306"
DB_NAME = os.environ['DB_NAME']

DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME
)
Engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
