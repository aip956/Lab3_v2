from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:local@db:5432/EngLab3"
# pwd = local; username = postgres

# engine = create_engine(SQLALCHEMY_DATABASE_URL) #Original
# engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=2, max_overflow=5, pool_timeout=10, pool_recycle=1800)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=4, max_overflow=5, pool_timeout=10, pool_recycle=1800)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

