from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Data, Base
import datetime

engine = create_engine('sqlite:///db.sqlite', echo=True)

Session = sessionmaker(bind=engine)
session = Session()


def add_data(label_type: str, label: str):
    data_row = Data(
        type=label_type,
        label=label,
        creation_date=datetime.datetime.now(),
        first_char=label[0].lower()
    )

    session.add(data_row)
    session.commit()


def get_random_result(first_char: str) -> list:
    return ['sddsa', 'dffdf', 'Fluss']


Base.metadata.create_all(engine)
