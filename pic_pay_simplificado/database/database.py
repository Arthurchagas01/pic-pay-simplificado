from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'postgresql://postgres:Admin123456+@localhost:5432/PicPaySimplificado'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
