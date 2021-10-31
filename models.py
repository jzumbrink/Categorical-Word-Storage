from sqlalchemy import Column, String, DATETIME, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    label = Column(String)
    creation_date = Column(DATETIME)
    first_char = Column(String)
    author = Column(Integer)
