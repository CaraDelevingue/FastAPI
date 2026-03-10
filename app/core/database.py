from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from urllib.parse import quote_plus
import os

#密码从环境变量中读取
DB_USER = os.getenv("DB_USER","root")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD","123456@abc"))
DB_HOST = os.getenv("DB_HOST","localhost")
DB_POST = os.getenv("DB_PORT",3306)
DB_NAME = os.getenv("DB_NAME","fastapi")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_POST}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()