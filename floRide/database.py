from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:ashu@localhost:3306/FloRide"
#SQLALCHEMY_DATABASE_URL is the database URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True
)
#engine is the starting point for any SQLAlchemy application

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#each instance of the session local class will be a database session
#the session is used to query the database, add objects to the database, and commit changes to the database
#the session is a temporary binding to the database

Base = declarative_base()
#we will inherit from this class to create each of the database models or classes (the ORM models)




