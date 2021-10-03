from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Data

engine = create_engine('sqlite:///db.sqlite', echo=True)

Session = sessionmaker(bind=engine)
session = Session()


def add_data(label_type, label):
    first_char = label[0]
