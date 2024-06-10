import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PASSWORD = os.environ.get("DB_PASSWORD")
if not DB_PASSWORD :
    print("DB_PASSWORD env variable is not set.")

SQLALCHEMY_DATABASE_URL = f"postgresql://silang-db-prod_owner:{DB_PASSWORD}@ep-frosty-grass-a1dij1jt.ap-southeast-1.aws.neon.tech/silang-db-prod?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
