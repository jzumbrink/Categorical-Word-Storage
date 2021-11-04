import datetime
import json
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Data, Base

engine = create_engine('sqlite:///db.sqlite', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())
    prefix = config['prefix']
    insertion_prefix = config['insertion-prefix']


def is_in_database(label_type: str, label: str, author_id: int) -> bool:
    result = session.query(Data).filter(Data.type == label_type, Data.label == label, Data.author == author_id)
    return result.count() > 0


def add_data(label_type: str, label: str, author_id: int) -> str:
    if is_in_database(label_type, label, author_id):
        return "Already in Database!"

    data_row = Data(
        type=label_type,
        label=label,
        creation_date=datetime.datetime.now(),
        first_char=label[0].lower(),
        author=author_id
    )

    session.add(data_row)
    session.commit()

    return f"\"{label}\" successfully added as {label_type}!"


def delete_data(label_type: str, label: str, author_id: int) -> str:
    if not is_in_database(label_type, label, author_id):
        return "Requested Object is not in the database!"
    result = list(session.query(Data).filter(Data.type == label_type, Data.label == label, Data.author == author_id))
    session.delete(result[0])
    session.commit()

    return f"The Object \"{label}\" from Type {label_type} was successfully deleted!"


def get_random_result(first_char: str, author_id: int) -> list:
    s_result = list(session.query(Data).filter(Data.first_char == first_char, Data.type == 's', Data.author == author_id))
    l_result = list(session.query(Data).filter(Data.first_char == first_char, Data.type == 'l', Data.author == author_id))
    f_result = list(session.query(Data).filter(Data.first_char == first_char, Data.type == 'f', Data.author == author_id))

    for result in [s_result, l_result, f_result]:
        if len(result) == 0:
            result.append(Data(label="--"))
        else:
            random.shuffle(result)

    return [s_result[0], l_result[0], f_result[0]]


def get_all(first_char: str, label_type: str, author_id: int) -> list:
    if first_char == '.':
        return list(session.query(Data).filter(Data.type == label_type, Data.author == author_id))
    else:
        return list(session.query(Data).filter(Data.type == label_type, Data.author == author_id, Data.first_char == first_char))


def get_rowcount() -> int:

    return session.query(Data).count()


def get_personal_rowcount(author_id: int) -> int:

    return session.query(Data).filter(Data.author == author_id).count()


def get_all_cats(author_id: int) -> list:
    cat_list = []
    for row in session.query(Data.type).filter(Data.author == author_id):
        category_str: str = row.type
        if category_str not in cat_list:
            cat_list.append(category_str)

    return cat_list