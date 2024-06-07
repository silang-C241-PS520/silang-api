from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Change user and password, create silang database for local development
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/silang"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
