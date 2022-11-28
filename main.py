import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = "postgresql://postgres:52449yfbkm@localhost:5432/netology_db2"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publisher_id = input('Введите id издателя ')

print("\nМагазины выбранного издателя: ")
subq = session.query(Book).join(Publisher.books).filter(Publisher.id == publisher_id).subquery()
for c in session.query(Shop).join(Stock).join(subq, Stock.id_book == subq.c.id).all():
    print(c)
