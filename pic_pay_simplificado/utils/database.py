from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'postgresql://postgres:your_password@localhost:5432/PicPaySimplificado'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

