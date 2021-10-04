from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Data, Base
import datetime, random

categories = {
    's': 'Stadt',
    'l': 'Land',
    'f': 'Fluss/Gewässer'
}

categories_en = {
    's': 'City',
    'l': 'Country',
    'f': 'River/Water'
}

engine = create_engine('sqlite:///db.sqlite', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def is_in_database(label_type: str, label: str) -> bool:
    return False


def add_data(label_type: str, label: str) -> str:
    if is_in_database(label_type, label):
        return "Already in Database!"

    data_row = Data(
        type=label_type,
        label=label,
        creation_date=datetime.datetime.now(),
        first_char=label[0].lower()
    )

    session.add(data_row)
    session.commit()

    return f"\"{label}\" successfully added as {categories_en[label_type]}!"


def get_random_result(first_char: str) -> list:
    s_result = list(session.query(Data).filter(Data.first_char == first_char, Data.type == 's'))
    l_result = list(session.query(Data).filter(Data.first_char == first_char, Data.type == 'l'))
    f_result = list(session.query(Data).filter(Data.first_char == first_char, Data.type == 'f'))

    for result in [s_result, l_result, f_result]:
        if len(result) == 0:
            result.append(Data(label="--"))
        else:
            random.shuffle(result)

    return [s_result[0], l_result[0], f_result[0]]
