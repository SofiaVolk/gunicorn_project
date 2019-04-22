import flask_marshmallow
from flask import Flask
import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow,Schema, fields, pprint
from sqlalchemy import CheckConstraint
from flask_marshmallow import Schema, fields #pip install flask-marshmallow
# docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=atom_pass -e MYSQL_DATABASE=atom_db -h 127.0.0.1 -d mysql
# mysql -u root -D atom_db -h 127.0.0.1 -p
DB_CONFIG = {
    'username': 'root',
    'password': 'atom_pass',
    'host': '127.0.0.1',
    'dbname': 'atom_db',
}
app = Flask(__name__)
# mysql+pymysql://username:password@server/db
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
    f"{DB_CONFIG['host']}/{DB_CONFIG['dbname']}?charset=utf8"
app.config['SQLALCHEMY_DATABASE_URI'] =f"mysql+pymysql://root:atom_pass@192.168.0.107:3336/atom_db"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class hh_domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'
    db.create_all()
    db.session.commit()


class hh_subdomain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_domain = db.Column(db.Integer, db.ForeignKey('hh_domain.id'))
    name = db.Column(db.String(80), nullable=False)
    hh_domain = relationship("hh_domain", backref="hh_subdomain", cascade="save-update, merge, delete",
                             primaryjoin='hh_domain.id==hh_subdomain.id_domain')

    def __repr__(self):
        return f'{self.id} {self.name}'
    db.create_all()
    db.session.commit()


class hh_sheldule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    db.create_all()
    db.session.commit()


class station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    db.create_all()
    db.session.commit()


class hh_company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    db.create_all()
    db.session.commit()


class cian_(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=False)
    count_rooms = db.Column(db.Integer)
    id_station = db.Column(db.Integer, ForeignKey('station.id'))
    price = db.Column(db.Numeric)
    floor = db.Column(db.Integer)
    square = db.Column(db.Numeric)
    price_sq = db.Column(db.Numeric)
    station = relationship("station", backref="cian_", cascade="save-update, merge, delete",
                           primaryjoin='station.id==cian_.id_station')
    CheckConstraint('price > 0', 'Цена должна быть больше 0!!')
    CheckConstraint('square*price_sq = price', 'Цена должна быть равной площади*цену за кв.метр!!')
    CheckConstraint('count_rooms > 0', 'Количество комнат больше 0!!')
    db.create_all()
    db.session.commit()
    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'


class hh_vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_company = db.Column(db.Integer, db.ForeignKey('hh_company.id'), nullable=False)
    id_scheldule = db.Column(db.Integer, db.ForeignKey('hh_sheldule.id'), nullable=False)
    salary = db.Column(db.Numeric, nullable=True)
    id_subdomain = db.Column(db.Integer,db.ForeignKey('hh_subdomain.id'), nullable=False)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    hh_company = db.relationship("hh_company", backref="hh_vacancy", cascade="save-update, merge, delete",
                                 primaryjoin='hh_company.id==hh_vacancy.id_company'
                                 )
    hh_sheldule = db.relationship("hh_sheldule", backref="hh_vacancy", cascade="save-update, merge, delete",
                             primaryjoin='hh_sheldule.id==hh_vacancy.id_scheldule')
    hh_subdomain = db.relationship("hh_subdomain", backref="hh_vacancy", cascade="save-update, merge, delete",
                             primaryjoin='hh_subdomain.id==hh_vacancy.id_subdomain')
    station = db.relationship("station", backref="hh_vacancy", cascade="save-update, merge, delete",
                                                     primaryjoin='station.id ==hh_vacancy.id_station')
    CheckConstraint('salary > 0', 'Зарплата должна быть больше 0!!)')

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    db.create_all()
    db.session.commit()


# class HhDomainSchema(ma.Schema):
#     id =ma.Schema.fields.Int(dump_only=True)
#     name = ma.fields.Str()
#
#
# class HhSubdomainSchema(ma.Schema):
#     id = ma.fields.Int(dump_only=True)
#     id_domain = ma.fields.Nested(HhDomainSchema,many = True)
#     name = ma.fields.Str()
#
#
# class HhShelduleSchema(ma.Schema):
#     id = ma.fields.Int(dump_only=True)
#     name = ma.fields.Str()
#
#
# class StationSchema(ma.Schema):
#     id = ma.fields.Int(dump_only=True)
#     name = ma.fields.Str()
#
#
# class HhCompanySchema(ma.Schema):
#     id = ma.fields.Int(dump_only=True)
#     name = ma.fields.Str()
#     contact = ma.fields.Str()
#
#
# class HhVacancySchema(ma.Schema):
#     id = ma.fields.Int(dump_only=True)
#     id_company = ma.fields.Nested(HhCompanySchema, many=True)
#     id_scheldule = ma.fields.Nested(HhShelduleSchema, many=True)
#     salary = ma.fields.Float()
#     id_subdomain = ma.fields.Nested(HhSubdomainSchema, many=True)
#     id_station = ma.fields.Nested(StationSchema, many=True)
#
#
# class CianSchema(ma.Schema):
#     id = ma.fields.Int(dump_only=True)
#     count_rooms = ma.fields.Int()
#     id_station = ma.fields.Nested(StationSchema, many=True)
#     price = ma.fields.Float()
#     floor = ma.fields.Int()
#     square = ma.fields.Float()
#     price_sq = ma.fields.Float()

# получить что то ################################################################################################


def get_id_station(name):
    if not station.query.filter_by(name=name).first():
        add_station(name)
    h=station.query.filter_by(name=name).all()
    return h[0].id


def get_id_subdomain(name,domain):
    if not hh_subdomain.query.filter_by(name=name).first():
        add_subdomain(name,domain)
    h=hh_subdomain.query.filter_by(name=name).all()
    return h[0].id


def get_id_sheldule(type):
    if not hh_sheldule.query.filter_by(type=type).first():
        add_sheldule(type)
    h = hh_sheldule.query.filter_by(type=type).all()
    return h[0].id


def get_id_company(name,contact):
    if not hh_company.query.filter_by(name=name).all():
        add_company(name,contact)
    h = hh_company.query.filter_by(name=name).all()
    return h[0].id


def get_id_domain(name):
    if not hh_domain.query.filter_by(name=name).first():
        add_domain(name)
    h = hh_domain.query.filter_by(name=name).all()
    return h[0].id


def get_domain(name=None):
    g=[]
    if name:
        g=hh_domain.query.filter_by(name=name).all()
        return g[0]
    else:
        g=hh_domain.quary.all()
        return g[0]


def get_company(name=None):
    if name:
        return hh_company.query.filter_by(name=name).all()
    else:
        return hh_company.quary.all()


def get_station(name=None):
    if name:
        return station.query.filter_by(name=name).all()
    else:
        return station.quary.all()


def get_sheldule(type=None):
    if type:
        return hh_sheldule.query.filter_by(name=type).all()
    else:
        return hh_sheldule.quary.all()


def get_subdomain(name=None):
    if name:
        return hh_subdomain.query.filter_by(name=name).all()
    else:
        return hh_subdomain.quary.all()


def get_vacancy(**data):  # всё по id
    if data:
        q = hh_vacancy.query()
        for attr, value in data.items():
            q = q.filter(getattr(hh_vacancy, attr).like("%%%s%%" % value))
    else:
        q = hh_vacancy.query.all()
    return q


def get_cian(**data):  # всё по id
    if data:
        q = cian_.query()
        for attr, value in data.items():
            q = q.filter(getattr(cian_, attr).like("%%%s%%" % value))
    else:
        q = cian_.query.all()
    return q

# обновления ################################################################################################


def update_station(name_old, name_now):
    station.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()


def update_subdomain(name_old, name_now, domain):
    if name_old and domain:
        id = get_id_domain(domain)
        if id:
            hh_subdomain.query.filter_by(name=name_old, id=id).update(name=name_now,id=id)
        else:
            raise('Такой области нет!!!!!!! Добавьте сначала область')
    if name_old:
        hh_subdomain.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()


def update_sheldule(type_old, type_now):
    hh_sheldule.query.filter_by(type=type_old).update(type=type_now)
    db.session.commit()


def update_company(name_old, name_now):
    hh_company.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()


def update_domain(name_old, name_now):
    hh_domain.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()

# добавить данные в таблицы########################################################################################

def add_station(name_now):
    db.session.add(station(name=name_now))
    db.session.commit()


def add_subdomain(name_now, domain):
    domain_id = get_id_domain(domain)
    if not domain_id:
        add_domain(domain)
    db.session.add(hh_subdomain(id_domain=domain_id, name=name_now))
    db.session.commit()


def add_sheldule(type_now):
    db.session.add(hh_sheldule(type=type_now))
    db.session.commit()


def add_company(name_now,contact):
    db.session.add(hh_company(name=name_now, contact=contact))
    db.session.commit()


def add_domain(name_now):
    db.session.add(hh_domain(id=1,name=name_now))
    db.session.commit()


def add_cian(id_cian, count_rooms, station, price, floor, square, pr_square):
    station_id = get_id_station(station)
    db.session.add(cian_(id=id_cian,count_rooms= count_rooms,id_station= station_id,price= price, floor=floor,
                         square=square,price_sq= pr_square))
    db.session.commit()


def add_vacancy(company, sceldule, salary, subdomain,station, domain=None, contact=None):
    station_id = get_id_station(station)
    id_company = get_id_company(company,contact)
    id_sceldule = get_id_sheldule(sceldule)
    id_subdomain = get_id_subdomain(subdomain,domain)
    db.session.add(hh_vacancy(id_company=id_company, id_scheldule=id_sceldule, salary=salary,
                              id_subdomain=id_subdomain, id_station=station_id))
    db.session.commit()

add_domain('IT')
# add_subdomain('engeneer','IT')
# add_company('kasper','654')
# add_sheldule('полный')
# add_station('каширская')
#add_vacancy('ert','пeолный',52600,'engeeeneer','кашир22ская','lskd','lskd')
#add_cian(65344,55,'кашgfирская',4300,1,4,100)