#import flask_marshmallow
from flask import Flask
import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship, session
#from flask_marshmallow import Marshmallow,Schema, fields, pprint
from sqlalchemy import CheckConstraint
#from  marshmallow import Schema, fields
#from flask_marshmallow import Schema, fields #pip install flask-marshmallow
# docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=atom_pass -e MYSQL_DATABASE=atom_db -h 127.0.0.1 -d mysql
# mysql -u root -D atom_db -h 127.0.0.1 -p
DB_CONFIG = {
    'username': 'root',
    'password': 'atom_pass',
    'host': '127.0.0.1',
    'port': '3336',
    'dbname': 'atom_db',
}
app = Flask(__name__)
# mysql+pymysql://username:password@server/db
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}?charset=utf8"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db = SQLAlchemy(app)
#ma = Marshmallow(app)


class HhDomain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'
    #db.create_all()
    #db.session.commit()alembic upgrade head


class HhSubdomain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_domain = db.Column(db.Integer, db.ForeignKey('hh_domain.id'))
    name = db.Column(db.String(80), nullable=False)
    hh_domain = relationship("hh_domain", backref="hh_subdomain", cascade="save-update, merge, delete",
                             primaryjoin='hh_domain.id==hh_subdomain.id_domain')

    def __repr__(self):
        return f'{self.id} {self.name}'
    #db.create_all()
    #db.session.commit()


# class HhSheldule(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.String(80), nullable=False)
#
#     def __repr__(self):
#         return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    #db.create_all()
    #db.session.commit()


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    #db.create_all()
    #db.session.commit()


class Curency(db.Model):#валюта в рублях
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    #db.create_all()
    #db.session.commit()


class HhCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=False)
    name = db.Column(db.String(80), nullable=False)
    #contact = db.Column(db.String(80), nullable=False)
    adress = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    #db.create_all()
    #db.session.commit()


class Cian(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=False)
    count_rooms = db.Column(db.String(80))
    id_station = db.Column(db.Integer, ForeignKey('station.id'))
    price = db.Column(db.Numeric)
    floor = db.Column(db.Integer)
    square = db.Column(db.Numeric)
    price_sq = db.Column(db.Numeric)
    adress = db.Column(db.String(200))
    station = relationship("station", backref="cian", cascade="save-update, merge, delete",
                           primaryjoin='station.id==cian.id_station')
    #db.create_all()
    #db.session.commit()
    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'


class HhVacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=False)
    id_company = db.Column(db.Integer, db.ForeignKey('hh_company.id'), nullable=False)
    #id_scheldule = db.Column(db.Integer, db.ForeignKey('hh_sheldule.id'), nullable=False)
    salary_min = db.Column(db.Numeric, nullable=True)
    salary_max = db.Column(db.Numeric, nullable=True)
    id_curency = db.Column(db.Integer, db.ForeignKey('curency.id'), nullable=True)
    id_subdomain = db.Column(db.Integer,db.ForeignKey('hh_subdomain.id'), nullable=False)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    hh_company = db.relationship("hh_company", backref="hh_vacancy", cascade="save-update, merge, delete",
                                 primaryjoin='hh_company.id==hh_vacancy.id_company'
                                 )
    curency = db.relationship("curency", backref="hh_vacancy", cascade="save-update, merge, delete",
                                 primaryjoin='curency.id==hh_vacancy.id_curency'
                                 )
    # hh_sheldule = db.relationship("hh_sheldule", backref="hh_vacancy", cascade="save-update, merge, delete",
    #                          primaryjoin='hh_sheldule.id==hh_vacancy.id_scheldule')
    hh_subdomain = db.relationship("hh_subdomain", backref="hh_vacancy", cascade="save-update, merge, delete",
                             primaryjoin='hh_subdomain.id==hh_vacancy.id_subdomain')
    station = db.relationship("station", backref="hh_vacancy", cascade="save-update, merge, delete",
                                                     primaryjoin='station.id ==hh_vacancy.id_station')

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    #db.create_all()
    #db.session.commit()


class CianUser(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=False)
    count_rooms = db.Column(db.String(80))
    id_station = db.Column(db.Integer, ForeignKey('station.id'))
    price = db.Column(db.Numeric)
    floor = db.Column(db.Integer)
    square = db.Column(db.Numeric)
    price_sq = db.Column(db.Numeric)
    adress = db.Column(db.String(200))
    station = relationship("station", backref="cian", cascade="save-update, merge, delete",
                           primaryjoin='station.id==cian.id_station')
    #db.create_all()
    #db.session.commit()
    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>, count_rooms =<{self.count_rooms}, >'\
    f'id_station = <{self.id_station}>, price = <{self.price}>, floor = <{self.floor}>, '\
    f'square = <{self.square}>, price_sq = <{self.price_sq}>, adress = <{self.adress}>'



class VacancyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement=False)
    id_company = db.Column(db.Integer, db.ForeignKey('hh_company.id'), nullable=False)
    #id_scheldule = db.Column(db.Integer, db.ForeignKey('hh_sheldule.id'), nullable=False)
    salary_min = db.Column(db.Numeric, nullable=True)
    salary_max = db.Column(db.Numeric, nullable=True)
    id_curency = db.Column(db.Integer, db.ForeignKey('curency.id'), nullable=True)
    id_subdomain = db.Column(db.Integer,db.ForeignKey('hh_subdomain.id'), nullable=False)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    hh_company = db.relationship("hh_company", backref="hh_vacancy", cascade="save-update, merge, delete",
                                 primaryjoin='hh_company.id==hh_vacancy.id_company'
                                 )
    curency = db.relationship("curency", backref="hh_vacancy", cascade="save-update, merge, delete",
                                 primaryjoin='curency.id==hh_vacancy.id_curency'
                                 )
    hh_sheldule = db.relationship("hh_sheldule", backref="hh_vacancy", cascade="save-update, merge, delete",
                             primaryjoin='hh_sheldule.id==hh_vacancy.id_scheldule')
    hh_subdomain = db.relationship("hh_subdomain", backref="hh_vacancy", cascade="save-update, merge, delete",
                             primaryjoin='hh_subdomain.id==hh_vacancy.id_subdomain')
    station = db.relationship("station", backref="hh_vacancy", cascade="save-update, merge, delete",
                                                     primaryjoin='station.id ==hh_vacancy.id_station')

    def __repr__(self):
        return f'{type(self).__name__} <{self.id}>=<{self.name}>'

    #db.create_all()
    #db.session.commit()


# получить что то ################################################################################################


def get_id_station(name):
    if not Station.query.filter_by(name=name).first():
        add_station(name)
    h=Station.query.filter_by(name=name).all()
    return h[0].id


def get_id_subdomain(name,domain):
    if not HhSubdomain.query.filter_by(name=name).first():
        add_subdomain(name,domain)
    h=HhSubdomain.query.filter_by(name=name).all()
    return h[0].id


# def get_id_sheldule(type):
#     if not HhSheldule.query.filter_by(type=type).first():
#         add_sheldule(type)
#     h = HhSheldule.query.filter_by(type=type).all()
#     return h[0].id
#

def get_id_curency(name):
    if not Curency.query.filter_by(name=name).first():
        add_curancy(type)
    h = Curency.query.filter_by(name=name).all()
    return h[0].id


def get_id_company(name,contact):
    if not HhCompany.query.filter_by(name=name).all():
        add_company(name,contact)
    h = HhCompany.query.filter_by(name=name).all()
    return h[0].id


def get_id_domain(name):
    if not HhDomain.query.filter_by(name=name).first():
        add_domain(name)
    h = HhDomain.query.filter_by(name=name).all()
    return h[0].id


def get_domain(name=None):
    g=[]
    if name:
        g=HhDomain.query.filter_by(name=name).all()
        return g[0]
    else:
        g=HhDomain.query.all()
        return g[0]


def get_company(name=None):
    if name:
        return HhCompany.query.filter_by(name=name).all()
    else:
        return HhCompany.quary.all()


def get_station(name=None):
    if name:
        return Station.query.filter_by(name=name).all()
    else:
        return Station.quary.all()

#
# def get_sheldule(type=None):
#     if type:
#         return HhSheldule.query.filter_by(name=type).all()
#     else:
#         return HhSheldule.quary.all()
#

def get_subdomain(name=None):
    if name:
        return HhSubdomain.query.filter_by(name=name).all()
    else:
        return HhSubdomain.quary.all()


def get_vacancy(**data):  # всё по id
    if data:
        q = HhVacancy.query()
        for attr, value in data.items():
            q = q.filter(getattr(HhVacancy, attr).like("%%%s%%" % value))
    else:
        q = HhVacancy.query.all()
    return q


def get_flat(**data):  # всё по id
    if data:
        q = Cian.query()
        for attr, value in data.items():
            q = q.filter(getattr(Cian, attr).like("%%%s%%" % value))
    else:
        q = session.query(CianUser).join('station').all()
    return q

# обновления ################################################################################################


def update_station(name_old, name_now):
    Station.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()


def update_subdomain(name_old, name_now, domain):
    if name_old and domain:
        id = get_id_domain(domain)
        if id:
           HhSubdomain.query.filter_by(name=name_old, id=id).update(name=name_now,id=id)
        else:
            raise('Такой области нет!!!!!!! Добавьте сначала область')
    if name_old:
        HhSubdomain.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()

#
# def update_sheldule(type_old, type_now):
#     HhSheldule.query.filter_by(type=type_old).update(type=type_now)
#     db.session.commit()


def update_company(name_old, name_now):
    HhCompany.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()


def update_domain(name_old, name_now):
    HhDomain.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()

# добавить данные в таблицы########################################################################################

def add_station(name_now):
    db.session.add(Station(name=name_now))
    db.session.commit()


def add_subdomain(name_now, domain):
    domain_id = get_id_domain(domain)
    if not domain_id:
        add_domain(domain)
    db.session.add(HhSubdomain(id_domain=domain_id, name=name_now))
    db.session.commit()


# def add_sheldule(type_now):
#     db.session.add(HhSheldule(type=type_now))
#     db.session.commit()


def add_company(name_now,contact):
    db.session.add(HhCompany(name=name_now, contact=contact))
    db.session.commit()


def add_domain(name_now):
    db.session.add(HhDomain(name=name_now))
    db.session.commit()


def add_curancy(name_now):
    db.session.add(Curency(name=name_now))
    db.session.commit()


def add_flat_user(count_rooms, station, price, floor, square, pr_square, adress):
    station_id = get_id_station(station)
    db.session.add(CianUser(count_rooms= count_rooms, id_station= station_id,price= price, floor=floor,
                         square=square,price_sq= pr_square, adress=adress))
    db.session.commit()


def add_flat(id_cian, count_rooms, station, price, floor, square, pr_square, adress):
    station_id = get_id_station(station)
    db.session.add(Cian(id=id_cian,count_rooms= count_rooms, id_station= station_id,price= price, floor=floor,
                         square=square,price_sq= pr_square, adress=adress))
    db.session.commit()


def add_vacancy_user(company, salary_min, salary_max, currency, subdomain, station, domain=None, contact=None):
    station_id = get_id_station(station)
    id_currency = get_id_curency(currency)
    id_company = get_id_company(company, contact)
    #id_sceldule = get_id_sheldule(sceldule)
    id_subdomain = get_id_subdomain(subdomain, domain)
    db.session.add(HhVacancy(id_company=id_company,  salary_min=salary_min,
                              salary_max=salary_max, id_curency=id_currency, id_subdomain=id_subdomain,
                              id_station=station_id))
    db.session.commit()


def add_vacancy(id, company, salary_min, salary_max, currency, subdomain, station, domain=None, contact=None):
    station_id = get_id_station(station)
    id_currency = get_id_curency(currency)
    id_company = get_id_company(company, contact)
    #id_sceldule = get_id_sheldule(sceldule)
    id_subdomain = get_id_subdomain(subdomain, domain)
    db.session.add(HhVacancy(id, id_company=id_company,  salary_min=salary_min,
                              salary_max=salary_max, id_curency=id_currency, id_subdomain=id_subdomain,
                              id_station=station_id))
    db.session.commit()


def del_flat_user(id):
    pass


def del_vacancy_user(id):
    pass


#примеры
add_domain('IT')
#add_subdomain('engeneer','IT')
#add_company('kasper','654')
#add_station('каширская')
#add_vacancy('ert','пeолный',52600,'engeeeneer','кашир22ская','lskd','lskd')
#add_cian(5344,'55','кашgfирская',400,5,4,100,'asdfsf')
#p=get_cian()
#print(p[0])
