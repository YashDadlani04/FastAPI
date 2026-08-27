from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url="postgresql://postgres:Qwerty098@localhost:5432/prod"
engine= create_engine(db_url)

session = sessionmaker(autocommit=False, autoflush=False, bind= engine)

