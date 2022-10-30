from flask import Flask, jsonify
from flask.views import MethodView
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask('app')
DSN = 'postgresql://postgres:postgres@127.0.0.1:5432/netology'
engine = create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class AdvertisementsModel(Base):

    __tablename__ = 'Advertisements'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    text = Column(String(300))
    create_time = Column(DateTime, server_default=func.now())
    owner = Column(String(32))


Base.metadata.create_all(engine)

class AdvertisementsView(MethodView):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


app.add_url_rule('/advt/', view_func=AdvertisementsView.as_view('advt'), methods=['GET', 'POST', 'DELETE'])

app.run()