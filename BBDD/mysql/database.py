from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3307/practica"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # TODO SOLO ES NECESARIO EN CASO DE USAR BSAE DE DATOS SQLITE , connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()