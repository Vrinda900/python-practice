import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session

load_dotenv()
DB_URL=os.getenv("DATABASE_URL", "sqlite:///patient.db")
connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
engine=create_engine(DB_URL, connect_args=connect_args)
sessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()