import pydantic as pydantic
from flask import Flask, jsonify, request
from typing import Type
from flask.views import MethodView
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask('app')


class HttpError(Exception):
    def __init__(self, status_code: int, msg: str | dict | list):
        self.status_code = status_code
        self.msg = msg


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({
        'status_code': 'error', 'msg': 'error.msg'
    })
    response = error.status_code
    return response


DSN = 'postgresql://postgres:postgres@127.0.0.1:5432/netology'
engine = create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    text = Column(String(300))
    create_time = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('owners.id'))
    owner = relationship(Owner, lazy='joined')


Base.metadata.create_all(engine)


class AdvertisementCheck(pydantic.BaseModel):
    name: str

    @pydantic.validator('name')
    def check_name(cls, value: str):
        if len('name') > 50:
            raise ValueError('length must be less then 50 chars')


def validate(date_to_validate: dict, validation_class: Type[AdvertisementCheck]):
    try:
        return validation_class(**date_to_validate).dict()

    except pydantic.ValidationError as err:
        raise HttpError(409, err.errors())


class AdvertisementsView(MethodView):
    def get(self, advertisements_id: int):
        with Session() as session:
            advertisement = session.query(Advertisement).get(advertisements_id)
            if advertisement is None:
                raise HttpError(404, 'ad is not found')
            return jsonify({
                'advt': advertisement.name,
                'advt_id': advertisement.id,
                'advt_text': advertisement.text
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            new_advt = Advertisement(**json_data)
            session.add(new_advt)
            session.commit()
            return jsonify({'status': 'ok', 'id': new_advt.id})

    def delete(self):
        pass


class OwnersView(MethodView):
    def get(self, owners_id: int):
        with Session() as session:
            owner = session.query(Owner).get(owners_id)
            if owner is None:
                raise HttpError(404, 'owner is not found')
            return jsonify({
                'owner': owner.name,
                'owner_id': owner.id
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            new_owner = Owner(**json_data)
            session.add(new_owner)
            session.commit()
            return jsonify({'status': 'ok', 'id': new_owner.id})

    def delete(self):
        pass


app.add_url_rule('/advt/', view_func=AdvertisementsView.as_view('advt_post'), methods=['POST'])
app.add_url_rule('/advt/<int:advertisements_id>/', view_func=AdvertisementsView.as_view('advt_get'), methods=['GET'])
app.add_url_rule('/owners/', view_func=OwnersView.as_view('owners_post'), methods=['POST'])
app.add_url_rule('/owners/<int:owners_id>/', view_func=OwnersView.as_view('owners_get'), methods=['GET'])
app.run()

