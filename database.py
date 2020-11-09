from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# from databases import Database


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False,'timeout': 15})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

Base = declarative_base()

# database = Database(SQLALCHEMY_DATABASE_URL)
