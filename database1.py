<<<<<<< HEAD
from sqlalchemy.orm import load_only, Load
from flask_sqlalchemy import SQLAlchemy
from flaskapp import app, str
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

=======
from sqlalchemy.orm import load_only, Load, relationship
# #from flask_sqlalchemy import SQLAlchemy
# from test_falcon import *
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
>>>>>>> gunicorn_ml
# docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=atom_pass -e MYSQL_DATABASE=atom_db -h 127.0.0.1 -d mysql
# docker ps
# docker exec -it pid bash
# mysql -u root -D atom_db -h 127.0.0.1 -p
# alter database atom_db character set=utf8mb4 collate utf8mb4_unicode_ci; --для кодировки нужной в бд
#  set names utf8mb4; -- чтобы в бд нормально отображалось всё
<<<<<<< HEAD
# 
db = SQLAlchemy(app)
Session = sessionmaker()
engine = create_engine(str)
=======
#

str1 = f"mysql+pymysql://root:atom_pass@127.0.0.1:3336/atom_db?charset=utf8mb4"
engine = create_engine(str1)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
db = declarative_base()
#db = SQLAlchemy(app)
#Session = sessionmaker()
#engine = create_engine(str)
>>>>>>> gunicorn_ml

# связываем его с нашим классом Session
Session.configure(bind=engine)

# работаем с сессией
session = Session()


<<<<<<< HEAD
class hh_domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


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
    title = db.Column(db.String(200))
    id_domain = db.Column(db.Integer, db.ForeignKey('hh_domain.id'))
    id_company = db.Column(db.Integer, db.ForeignKey('hh_company.id'))
    description = db.Column(db.String(10000))
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
=======
class hh_domain(db):
    __tablename__ = 'hh_domain'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class station(db):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class curency(db):
    __tablename__ = 'curency'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class hh_company(db):
    __tablename__ = 'hh_company'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class hh_vacancy(db):
    __tablename__ = 'hh_vacancy'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    id_domain = Column(Integer, ForeignKey('hh_domain.id'))
    id_company = Column(Integer, ForeignKey('hh_company.id'))
    description = Column(String(10000))
    salary_min = Column(Numeric)
    salary_max = Column(Numeric)
    id_curency = Column(Integer, ForeignKey('curency.id'))
    id_station = Column(Integer, ForeignKey('station.id'))

    hh_company = relationship("hh_company", backref="hh_vacancy", cascade="save-update, merge, delete",
                                 primaryjoin='hh_company.id==hh_vacancy.id_company'
                                 )
    hh_domain = relationship("hh_domain", backref="hh_vacancy", cascade="save-update, merge, delete",
                             primaryjoin='hh_domain.id==hh_vacancy.id_domain')
    station =relationship("station", backref="hh_vacancy", cascade="save-update, merge, delete",
                                                     primaryjoin='station.id ==hh_vacancy.id_station')
    curency = relationship("curency", backref="hh_vacancy", cascade="save-update, merge, delete",
                              primaryjoin='curency.id ==hh_vacancy.id_curency')

'''
class hh_vacancy_user(db):
    id = db.Column(Integer, primary_key=True)
>>>>>>> gunicorn_ml
    name = db.Column(db.String(200))
    id_domain = db.Column(db.Integer, db.ForeignKey('hh_domain.id'))
    id_company = db.Column(db.Integer, db.ForeignKey('hh_company.id'))
    about = db.Column(db.String(10000))
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

<<<<<<< HEAD

class youla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    description = db.Column(db.String(100000))
    product_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    subcategory_id = db.Column(db.Integer)
    properties = db.Column(db.String(10000))
    image_links = db.Column(db.String(10000))

=======
'''
class youla(db):
    __tablename__ = 'youla'
    id = Column(Integer, primary_key=True)
    title = Column(String(10000))
    description = Column(String(100000))
    product_id = Column(Integer)
    category_id = Column(Integer)
    subcategory_id = Column(Integer)
    properties = Column(String(10000))
    image_links = Column(String(10000))


class users(db):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    password = Column(String(10000))
    mail = Column(String(100000))
>>>>>>> gunicorn_ml
# получить что то ################################################################################################


def get_id_station(name):
<<<<<<< HEAD
    if not station.query.filter_by(name=name).first():
        add_station(name)
    h=station.query.filter_by(name=name).first()
=======
    if not Session.query(station).filter_by(name=name).first():
        add_station(name)
    h=Session.query(station).filter_by(name=name).first()
>>>>>>> gunicorn_ml
    return h.id


def get_id_company(name):
<<<<<<< HEAD
    if not hh_company.query.filter_by(name=name).first():
        add_company(name)
    h = hh_company.query.filter_by(name=name).first()
=======
    if not Session.query(hh_company).filter_by(name=name).first():
        add_company(name)
    h = Session.query(hh_company).filter_by(name=name).first()
>>>>>>> gunicorn_ml
    return h.id


def get_id_domain(name):
<<<<<<< HEAD
    if not hh_domain.query.filter_by(name=name).first():
        add_domain(name)
    h = hh_domain.query.filter_by(name=name).first()
=======
    if not Session.query(hh_domain).filter_by(name=name).first():
        add_domain(name)
    h = Session.query(hh_domain).filter_by(name=name).first()
>>>>>>> gunicorn_ml
    return h.id


def get_id_curency(name):
<<<<<<< HEAD
    if not curency.query.filter_by(name=name).first():
        add_curency(name)
    h = curency.query.filter_by(name=name).first()
=======
    if not  Session.query(curency).filter_by(name=name).first():
        add_curency(name)
    h = Session.query(curency).filter_by(name=name).first()
>>>>>>> gunicorn_ml
    return h.id


def get_domain(name=None):
<<<<<<< HEAD
    qs = hh_domain.query
=======
    qs = Session.query(hh_domain)
>>>>>>> gunicorn_ml

    if name:
        qs = qs.filter_by(name=name)

    return qs.all()


def get_company(name=None):
    if name:
<<<<<<< HEAD
        return hh_company.query.filter_by(name=name).first()
    else:
        return hh_company.quary.first()
=======
        return Session.query(hh_company).filter_by(name=name).first()
    else:
        return Session.quary(hh_company).first()
>>>>>>> gunicorn_ml


def get_station(name=None):
    if name:
<<<<<<< HEAD
        return station.query.filter_by(name=name).first()
    else:
        return station.quary.first()


def get_vacancy(id):  # всё по id
    q = hh_vacancy.query.filter_by(id=id).first()
=======
        return Session.query(station).filter_by(name=name).first()
    else:
        return Session.quary(station).first()


def get_vacancy(id):  # всё по id
    q = Session.query(hh_vacancy).filter_by(id=id).first()
>>>>>>> gunicorn_ml
    return q

# для ml #####################################################################################################


<<<<<<< HEAD
def get_vacancies(hh_vac,hh_dom): # 2 лист из списка нужных полей
    c = []
    ii = 0
    for cc, i in session.query(hh_vacancy, hh_domain).join(hh_domain)\
            .options(
            Load(hh_vacancy).load_only(*hh_vac),
            Load(hh_domain).load_only(*hh_dom)
            ).all():
        d = cc.__dict__
        d.update(i.__dict__)
        c.append(d)
        c[ii].pop("_sa_instance_state")
        ii = ii+1
    return c  # возвращает список из словарей выбранных полей


'''
c=['title',"description"]
cc=["name"]
get_vacancies(c,cc)
'''
=======
def get_vacancies(hh_vac,hh_dom=None): # 2 лист из списка нужных полей
    c = []
    ii = 0
    if hh_dom is not None:
        for cc, i in Session.query(hh_vacancy, hh_domain).join(hh_domain) \
                .options(
            Load(hh_vacancy).load_only(*hh_vac),
            Load(hh_domain).load_only(*hh_dom)
        ).all():
            d = cc.__dict__
            d.update(i.__dict__)
            c.append(d)
            c[ii].pop("_sa_instance_state")
            ii = ii + 1
    else:
        for cc in Session.query(hh_vacancy).join(hh_domain) \
                .options(
            Load(hh_vacancy).load_only(*hh_vac),

        ).all():
            d = cc.__dict__
            c.append(d)
            c[ii].pop("_sa_instance_state")
            ii = ii + 1


    return c  # возвращает список из словарей выбранных полей



#c=['title',"description"]
#cc=[None]
#get_vacancies(c)

>>>>>>> gunicorn_ml


def get_youla(kwargs):  # лист из списка нужных полей
    c = []
    ii = 0
<<<<<<< HEAD
    for i in session.query(youla).options(load_only(*kwargs)).all():
=======
    for i in Session.query(youla).options(load_only(*kwargs)).all():
>>>>>>> gunicorn_ml
        c.append(i.__dict__)
        c[ii].pop("_sa_instance_state")
        ii = ii + 1
    return c  # возвращает список из словарей выбранных полей

<<<<<<< HEAD

def get_list_youla(kwargs):  # лист из списка нужных полей
    c = []
    ii = 0
    for i in session.query(youla).filter(youla.id.in_(kwargs)).all():
=======
#c=['title',"description"]
#cc=[None]
#get_youla(c)
def get_list_youla(kwargs):  # лист из списка нужных полей
    c = []
    ii = 0
    for i in Session.query(youla).filter(youla.id.in_(kwargs)).all():
>>>>>>> gunicorn_ml
        c.append(i.__dict__)
        c[ii].pop("_sa_instance_state")
        ii = ii + 1
    return c  # возвращает список из словарей выбранных полей


def get_list_vacancy(kwargs):  # лист из списка нужных полей
    c = []
    ii = 0
<<<<<<< HEAD
    for i in session.query(hh_vacancy).filter(hh_vacancy.id.in_(kwargs)).all():
=======
    for i in Session.query(hh_vacancy).filter(hh_vacancy.id.in_(kwargs)).all():
>>>>>>> gunicorn_ml
        c.append(i.__dict__)
        c[ii].pop("_sa_instance_state")
        ii = ii + 1
    return c  # возвращает список из словарей выбранных полей

# get_list_vacancy(["1","3","6","7"])
# get_list_youla(["1","3","6","7"])
# def vacancy_for_user(args):
#     c = []
#     ii = 0
#     for i in session.query(hh_vacancy).filter_by(hh_vacancy.id.in_(*args)).all():
#         c.append(i.__dict__)
#         c[ii].pop("_sa_instance_state")
#         ii = ii + 1
#     return c
#
# g=[12,15]
# vacancy_for_user(g)
# удаление ################################################################################################


def del_vacancy_user(id):
<<<<<<< HEAD
    db.session.delete(hh_vacancy(id=id))
    db.session.commit()


def del_youla_user(id):
    db.session.delete(youla(id=id))
    db.session.commit()
=======
    Session.delete(hh_vacancy(id=id))
    Session.commit()


def del_youla_user(id):
    Session.delete(youla(id=id))
    Session.commit()
>>>>>>> gunicorn_ml

# обновления ################################################################################################


def update_station(name_old, name_now):
<<<<<<< HEAD
    station.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()


def update_company(name_old, name_now):
    hh_company.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()


def update_domain(name_old, name_now):
    hh_domain.query.filter_by(name=name_old).update(name=name_now)
    db.session.commit()
=======
    Session.query(station).filter_by(name=name_old).update(name=name_now)
    Session.commit()


def update_company(name_old, name_now):
    Session.query(hh_company).filter_by(name=name_old).update(name=name_now)
    Session.commit()


def update_domain(name_old, name_now):
    Session.query(hh_domain).filter_by(name=name_old).update(name=name_now)
    Session.commit()
>>>>>>> gunicorn_ml

# добавить данные в таблицы########################################################################################


def add_station(name_now):
<<<<<<< HEAD
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
=======
    Session.add(station(name=name_now))
    Session.commit()


def add_company(name_now):
    Session.add(hh_company(name=name_now))
    Session.commit()


def add_curency(name_now):
    Session.add(curency(name=name_now))
    Session.commit()


def add_domain(name_now):
    Session.add(hh_domain(name=name_now))
    Session.commit()
>>>>>>> gunicorn_ml


def add_vacancy(id, title, domain, company=None, description=None, salary_min=None, salary_max=None,
                curency=None, station=None ):
        station_id = get_id_station(station) if station!=None else None
        id_company = get_id_company(company) if company!=None else None
        id_curency = get_id_curency(curency) if curency!=None else None
        id_domain = get_id_domain(domain)    if domain!=None else None
<<<<<<< HEAD
        db.session.add(hh_vacancy(title=title
=======
        Session.add(hh_vacancy(title=title
>>>>>>> gunicorn_ml
                                  , id_domain=id_domain
                                  , id_company=id_company
                                  , description=description
                                  , salary_min=salary_min
                                  , salary_max=salary_max
                                  , id_curency=id_curency
                                  , id_station=station_id
                                  )
                       )
<<<<<<< HEAD
        db.session.commit()


def add_youla(title, description, product_id, category_id, subcategory_id, properties, image_links):
    db.session.add(youla(title=title
=======
        Session.commit()


def add_youla(title, description, product_id, category_id, subcategory_id, properties, image_links):
    Session.add(youla(title=title
>>>>>>> gunicorn_ml
                          , description=description
                          , product_id=product_id
                          , category_id=category_id
                          , subcategory_id=subcategory_id
                          , properties=properties
                          , image_links=image_links
                          )
                   )
<<<<<<< HEAD
    db.session.commit()


=======
    Session.commit()


def add_users(password, mail):
    try:
        Session.add(users(password=password,
                          mail=mail
                              )
                       )
        Session.commit()
        return True
    except:
        return None

####################check user
def check_users(mail,password):
    user=Session.query(hh_company).filter_by(mail=mail,password=password).first()
    if user:
        return True
    else:
        return False

>>>>>>> gunicorn_ml
#add_vacancy(123,'ksdj',1,'IT','ert','ljhlkjfhslf',52600,654654,'engeeeneer','кашир22ская')
