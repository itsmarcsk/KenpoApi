from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:root@localhost:3307/tfc"
SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:root@172.18.0.4:3306/tfc"


# Crea el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()