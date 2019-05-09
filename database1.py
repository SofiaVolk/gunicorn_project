from flask import Flask
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_marshmallow import Marshmallow,Schema, fields, pprint
# docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=atom_pass -e MYSQL_DATABASE=atom_db -h 127.0.0.1 -d mysql
# mysql -u root -D atom_db -h 127.0.0.1 -p
# alter database atom_db character set=utf8mb4 collate utf8mb4_unicode_ci; --для кодировки нужной в бд
#  set names utf8mb4; -- чтобы в бд нормально отображалось всё
#
DB_CONFIG = {
    'username': 'root',
    'password': 'atom_pass',
    'host': '127.0.0.1',
    'dbname': 'atom_db',
}
app = Flask(__name__)
# mysql+pymysql://username:password@server/db
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
    f"{DB_CONFIG['host']}/{DB_CONFIG['dbname']}?charset=utf8mb4"
app.config['SQLALCHEMY_DATABASE_URI'] =f"mysql+pymysql://root:atom_pass@127.0.0.1/atom_db?charset=utf8mb4"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class hh_domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # def __repr__(self):
    #     return f'{type(self).__name__} <{self.id}>=<{self.name}>'
    # db.create_all()
    # db.session.commit()

class station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class curency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class hh_company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class hh_vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200)),
    id_domain = db.Column(db.Integer, db.ForeignKey('hh_domain.id'))
    id_company = db.Column(db.Integer, db.ForeignKey('hh_company.id'))
    about = db.Column(db.String(10000)),
    salary_min = db.Column(db.Numeric)
    salary_max = db.Column(db.Numeric)
    id_curency = db.Column(db.Integer, db.ForeignKey('curency.id'))
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    hh_company = db.relationship("hh_company", backref="hh_vacancy", cascade="save-update, merge, delete",
                                 primaryjoin='hh_company.id==hh_vacancy.id_company'
                                 )
    hh_domain = db.relationship("hh_domain", backref="hh_vacancy", cascade="save-update, merge, delete",
                             primaryjoin='hh_domain.id==hh_vacancy.id_domain')
    station = db.relationship("station", backref="hh_vacancy", cascade="save-update, merge, delete",
                                                     primaryjoin='station.id ==hh_vacancy.id_station')
    curency = db.relationship("curency", backref="hh_vacancy", cascade="save-update, merge, delete",
                              primaryjoin='curency.id ==hh_vacancy.id_curency')

class hh_vacancy_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200)),
    id_domain = db.Column(db.Integer, db.ForeignKey('hh_domain.id'))
    id_company = db.Column(db.Integer, db.ForeignKey('hh_company.id'))
    about = db.Column(db.String(10000)),
    salary_min = db.Column(db.Numeric)
    salary_max = db.Column(db.Numeric)
    id_curency = db.Column(db.Integer, db.ForeignKey('curency.id'))
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    hh_company = db.relationship("hh_company", backref="hh_vacancy_user", cascade="save-update, merge, delete",
                                 primaryjoin='hh_company.id==hh_vacancy_user.id_company'
                                 )
    hh_domain = db.relationship("hh_domain", backref="hh_vacancy_user", cascade="save-update, merge, delete",
                                primaryjoin='hh_domain.id==hh_vacancy_user.id_domain')
    station = db.relationship("station", backref="hh_vacancy_user", cascade="save-update, merge, delete",
                              primaryjoin='station.id ==hh_vacancy_user.id_station')
    curency = db.relationship("curency", backref="hh_vacancy_user", cascade="save-update, merge, delete",
                              primaryjoin='curency.id ==hh_vacancy_user.id_curency')

class youla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000)),
    descrirption = db.Column(db.String(100000))
    product_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer),
    subcategory_id = db.Column(db.Integer)
    properties = db.Column(db.String(10000))
    image_links = db.Column(db.String(10000))

# получить что то ################################################################################################


def get_id_station(name):
    if not station.query.filter_by(name=name).first():
        add_station(name)
    h=station.query.filter_by(name=name).first()
    return h[0].id

def get_id_company(name):
    if not hh_company.query.filter_by(name=name).first():
        add_company(name)
    h = hh_company.query.filter_by(name=name).first()
    return h[0].id

def get_id_domain(name):
    if not hh_domain.query.filter_by(name=name).first():
        add_domain(name)
    h = hh_domain.query.filter_by(name=name).first()
    return h[0].id

def get_id_curency(name):
    if not curency.query.filter_by(name=name).first():
        add_curency(name)
    h = curency.query.filter_by(name=name).first()
    return h[0].id

def get_domain(name=None):
    g=[]
    if name:
        g=hh_domain.query.filter_by(name=name).first()
        return g[0]
    else:
        g=hh_domain.quary.all()
        return g[0]

def get_company(name=None):
    if name:
        return hh_company.query.filter_by(name=name).first()
    else:
        return hh_company.quary.first()


def get_station(name=None):
    if name:
        return station.query.filter_by(name=name).first()
    else:
        return station.quary.first()

def get_vacancy(id):  # всё по id
    q = hh_vacancy.query.filter_by(id=id).first()
    return q


# удаление ################################################################################################

def del_vacancy_user(id):
    db.session.delete(hh_vacancy(id=id))
    db.session.commit()


def del_youla_user(id):
    db.session.delete(youla(id=id))
    db.session.commit()

# обновления ################################################################################################


def update_station(name_old, name_now):
    station.query.filter_by(name=name_old).update(name=name_now)
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


def add_company(name_now):
    db.session.add(hh_company(name=name_now))
    db.session.commit()


def add_curency(name_now):
    db.session.add(curency(name=name_now))
    db.session.commit()

def add_domain(name_now):
    db.session.add(hh_domain(name=name_now))
    db.session.commit()


def add_vacancy(id,name, domain,company=None, about=None, salary_min=None,salary_max=None, curency=None, station=None ):
        station_id = get_id_station(station) if station!=None else None
        id_company = get_id_company(company) if company!=None else None
        id_curency = get_id_curency(curency) if curency!=None else None
        id_domain = get_id_domain(domain)    if domain!=None else None
        db.session.add(hh_vacancy(id=id, name=name
                                  , id_domain=id_domain
                                  , id_company=id_company
                                  , about=about
                                  , salary_min=salary_min
                                  , salary_max=salary_max
                                  , id_curency=id_curency
                                  , id_station=station_id
                                  )
                       )
        db.session.commit()


def add_youla(title, descrirption,product_id, category_id, subcategory_id,properties, image_links):
    db.session.add(youla( title=title
                          , descrirption=descrirption
                          , product_id=product_id
                          , category_id=category_id
                          , subcategory_id=subcategory_id
                          , properties=properties
                          , image_links=image_links
                          )
                   )
    db.session.commit()


#add_vacancy(123,'ksdj',1,'IT','ert','ljhlkjfhslf',52600,654654,'engeeeneer','кашир22ская')
