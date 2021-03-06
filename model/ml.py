from pymorphy2 import MorphAnalyzer
from os import path, remove, getcwd
from re import findall
from functools import lru_cache
from gensim.models import KeyedVectors
from annoy import AnnoyIndex
import pandas as pd
import numpy as np
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from pickle import dump, load
from sklearn.neighbors import KNeighborsClassifier
from project_atom_app.database1 import get_youla, get_vacancies

CRITICAL_SIMILARITY = 0.75
NULL_VECTOR = np.zeros(300)

with open("/home/sonya/gunicorn-master/project_atom_app/model/.data/categories_dict.pkl", "rb") as f:
    categories_dict = load(f)

with open("/home/sonya/gunicorn-master/project_atom_app/model/.data/categories_model.pkl", "rb") as f:
    categories_model = load(f)

with open("/home/sonya/gunicorn-master/project_atom_app/model/.data/dummy_model.pkl", "rb") as f:
    dummy_model = load(f)

w2v_model = KeyedVectors.load_word2vec_format(
    "/home/sonya/gunicorn-master/project_atom_app/model/.data/araneum_upos_skipgram_300_2_2018.vec")

with open("/home/sonya/gunicorn-master/project_atom_app/model/.data/stopwords.txt", "r") as f:
    stopwords = f.read().split()

hh_annoy = AnnoyIndex(300)
hh_annoy.load("/home/sonya/gunicorn-master/project_atom_app/model/.data/hh_annoy.ann")

youla_annoy = AnnoyIndex(300)
youla_annoy.load("/home/sonya/gunicorn-master/project_atom_app/model/.data/youla_annoy.ann")

morph = MorphAnalyzer()


class Model:

    @staticmethod
    @lru_cache(maxsize=10000)
    def get_normal_form(word):
        """
        Получение нормальной формы слова
        :param word: слово в виде строки
        :return: нормальная форма от pymorpy2
        """
        p = morph.parse(word)[0]
        try:
            p = p.normal_form + '_' + p.tag.POS
        except Exception as e:
            print(str(e) + " на слове " + p.normal_form)
            p = p.normal_form
        return p

    @staticmethod
    def text2vec(text):
        """
        Векторизация текста
        :param text: текст в виде строки
        :return: вектор слова от Word2Vec
        """
        words = [Model.get_normal_form(i) for i in findall('\w+', text)
                 if ((not i.isdigit()) and (len(i) > 2) and
                     (i not in stopwords))]
        result = np.zeros(w2v_model.vector_size)
        for i in words:
            try:
                result += w2v_model[i]
            except KeyError:
                pass
        return result

    def knn_youla(self, text, number=10):
        """
        Поиск похожих вещей
        :param text: текст в виде строки
        :param number: число похожих объявлений
        :return: список номеров строк похожих объявлений в бд
        """
        return youla_annoy.get_nns_by_vector(
            self.text2vec(text), number)

    def knn_hh(self, text, number=10):
        """
        Поиск похожих вакансий
        :param text: текст в виде строки
        :param number: число похожих объявлений
        :return: список номеров строк похожих объявлений в бд
        """
        return hh_annoy.get_nns_by_vector(
            self.text2vec(text), number)

    def wish_detector(self, text):
        """
        Определение типа хотелки
        :param text: текст хотелки
        :return: тип хотелки
        """
        vector = self.text2vec(text)
        null_vector = np.zeros(300)
        if (vector == null_vector).all():
            return "dummy"
        decision = dummy_model.predict_proba([vector])[0]
        print(decision)
        if decision[1] >= CRITICAL_SIMILARITY:
            return 'youla'
        elif decision[0] >= CRITICAL_SIMILARITY:
            return 'hh'
        else:
            return 'dummy'

    def wish_handler(self, text, number=10):
        """
        Обработка хотелки и выдача похожих результатов
        :param text: текст в виде строки
        :param number: число похожих результатов
        :return: тип хотелки, список номеров строк в бд
        """
        vector = self.text2vec(text)
        if (vector == NULL_VECTOR).all():
            return "dummy", list()
        decision = dummy_model.predict_proba([vector])[0]
        if decision[1] >= CRITICAL_SIMILARITY:
            return 'youla', self.knn_youla(text, number)
        elif decision[0] >= CRITICAL_SIMILARITY:
            return 'hh', self.knn_hh(text, number)
        else:
            return 'dummy', list()

    def predict(self, id):
        """
        Предсказание категории объявление
        :param id: уникальный номер объявления
        :return: category_id, category_name
        """
        category_id = categories_model.predict([hh_annoy.get_item_vector(id)])[0]
        return category_id, categories_dict[category_id]

    def predict_text(self, text):
        """
        Предсказание категории объявление
        :param id: уникальный номер объявления
        :return: category_id, category_name
        """
        vector = self.text2vec(text)
        category_id = categories_model.predict([vector])[0]
        return category_id, categories_dict[category_id]


def dump_all():
    """
    Дамп всего
    """
    dump_hh()
    print("hh")
    dump_youla()
    print("youla")
    dump_categories()
    print("categories")
    dump_dummy()
    print("dummy")


def dump_hh():
    """
    Сохранение данных с базы hh
    """
    data = pd.DataFrame(get_vacancies(["title", "description"]))
    data.title.fillna('', inplace=True)
    data.description.fillna(data.title, inplace=True)
    data['text'] = data.title + ' ' + data.description
    vec = np.empty((data.shape[0], 300), dtype=np.float)
    for i in range(data.shape[0]):
        vec[i] = Model.text2vec(data.iloc[i]['text'])
    new_hh_annoy = AnnoyIndex(300)
    for i, j in enumerate(vec):
        new_hh_annoy.add_item(data.iloc[i]["id"], j)
    new_hh_annoy.build(10)
    annoy_path = "/home/sonya/gunicorn-master/project_atom_app/model/.data/hh_annoy.ann"
    if path.isfile(annoy_path):
        remove(annoy_path)
    new_hh_annoy.save(annoy_path)


def dump_youla():
    """
    Сохранение данных с базы юлы
    """
    data = pd.DataFrame(get_youla(["title", "description"]))
    data.title.fillna('', inplace=True)
    data.description.fillna(data.title, inplace=True)
    data['text'] = data.title + ' ' + data.description
    vec = np.empty((data.shape[0], 300), dtype=np.float)
    for i in range(data.shape[0]):
        vec[i] = Model.text2vec(data.iloc[i]['text'])
    new_youla_annoy = AnnoyIndex(300)
    for i, j in enumerate(vec):
        new_youla_annoy.add_item(data.iloc[i]["id"], j)
    new_youla_annoy.build(10)
    annoy_path = "/home/sonya/gunicorn-master/project_atom_app/model/.data/youla_annoy.ann"
    if path.isfile(annoy_path):
        remove(annoy_path)
    new_youla_annoy.save(annoy_path)


def dump_categories():
    """
    Сохранение категорий и переобучение предсказалки
    """
    data = pd.DataFrame(get_vacancies(["title", "description", "id_domain"], ["name"]))
    cats = data.drop_duplicates(subset='id_domain')
    new_categories_dict = dict()
    for i in cats[['id_domain', 'name']].values:
        new_categories_dict[i[0]] = i[1]
    with open("/home/sonya/gunicorn-master/project_atom_app/model/.data/categories_dict.pkl", "wb+") as f:
        dump(new_categories_dict, f)
    data = data.sample(10000)
    data.title.fillna(data.description, inplace=True)
    data['text'] = data.title
    vec = np.empty((data.shape[0], 300), dtype=np.float)
    for i in range(data.shape[0]):
        vec[i] = Model.text2vec(data.iloc[i]['text'])
    new_categories_model = BaggingClassifier(DecisionTreeClassifier(min_samples_leaf=5))
    new_categories_model.fit(vec, data['id_domain'].values)
    with open("/home/sonya/gunicorn-master/project_atom_app/model/.data/categories_model.pkl", "wb+") as f:
        dump(new_categories_model, f)


def dump_dummy():
    """
    Сохранение решающей модели
    """
    data_hh = pd.DataFrame(get_vacancies(["title", "description"])).sample(10000)
    data_youla = pd.DataFrame(get_youla(["title", "description"])).sample(10000)
    for data in [data_hh, data_youla]:
        data.title.fillna(data.description, inplace=True)
        data['text'] = data.title
    vec = np.empty((data_hh.shape[0] + data_youla.shape[0], 300), dtype=np.float)
    ids = np.zeros(data_hh.shape[0] + data_youla.shape[0], dtype=np.int)
    for i in range(data_hh.shape[0]):
        vec[i] = Model.text2vec(data_hh.iloc[i]['text'])
    for i in range(data_youla.shape[0]):
        vec[i + data_hh.shape[0]] = Model.text2vec(data_youla.iloc[i]['text'])
        ids[i + data_hh.shape[0]] = 1
    new_dummy_model = KNeighborsClassifier()
    new_dummy_model.fit(vec, ids)
    with open("/home/sonya/gunicorn-master/project_atom_app/model/.data/dummy_model.pkl", "wb+") as f:
        dump(new_dummy_model, f)

# dump_all()
