from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from configparser import ConfigParser

config = ConfigParser()
config.read('../database.ini')
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=config.get('postgresql', 'user'), pw=config.get('postgresql','password'), url=config.get('postgresql', 'host')+":"+config.get('postgresql', 'port'), db=config.get('postgresql', 'database'))

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()