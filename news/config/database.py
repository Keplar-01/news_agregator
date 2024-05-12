from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
db_url = 'postgresql://root:root@postgres:5432/news_db'

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()