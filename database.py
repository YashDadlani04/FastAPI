import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/prod")
engine = create_engine(db_url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

