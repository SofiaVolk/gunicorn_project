from pymorphy2 import MorphAnalyzer
from re import findall
from functools import lru_cache
from gensim.models import KeyedVectors
from annoy import AnnoyIndex
import pandas as pd
from os import path, listdir
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from pickle import dump, load
from datetime import datetime
from alembic.database import get_youla, get_hh

CRITICAL_COSINE_SIMILARITY = 0.30
CATEGORIES_DICT_FOLDER = path.join(".data/categories_dict/")
HH_ANNOY_FOLDER = path.join(".data/hh_annoy/")
YOULA_ANNOY_FOLDER = path.join(".data/youla_annoy/")
KNN_MODEL_FOLDER = path.join(".data/knn_model/")
W2V_MODEL_FILE = path.join(".data/w2v_model/araneum_none_fasttextskipgram_300_5_2018.model")
STOPWORDS_FILE = path.join(".data/stopwords.txt")


class Model:

    def __init__(self, knn_model_filename=None,
                 youla_annoy_filename=None, hh_annoy_filename=None,
                 categories_dict_filename=None):
        # для нормализации текста
        self.morph = MorphAnalyzer()
        # стоп слова
        self.stopwords = None
        self._load_stopwords()
        # вектора таблиц
        self.youla_annoy = None
        self.hh_annoy = None
        self._load_youla_annoy(youla_annoy_filename)
        self._load_hh_annoy(hh_annoy_filename)
        # обученный Word2Vec
        self.w2v_model = None
        self._load_w2v_model()
        # словарь с категориями
        self.categories_dict = None
        self._load_categories_dict(categories_dict_filename)
        # обученный KNeighborsClassifier
        self.knn_model = None
        self._load_knn_model(knn_model_filename)
        # вектора для определения типа хотелки
        self.hh_vectors = None
        self.youla_vectors = None
        self._load_dummy_vectors()

    @lru_cache(maxsize=10000)
    def get_normal_form(self, word):
        """
        Получение нормальной формы слова
        :param word: слово в виде строки
        :return: нормальная форма от pymorpy2
        """
        return self.morph.normal_forms(word)[0]

    def text2vec(self, text):
        """
        Векторизация текста
        :param text: текст в виде строки
        :return: вектор слова от Word2Vec
        """
        words = [self.get_normal_form(i) for i in findall('\w+', text)
                 if ((not i.isdigit()) and (len(i) > 2) and
                     (i not in self.stopwords))]
        result = np.zeros(self.w2v_model.vector_size)
        for i in words:
            try:
                result += self.w2v_model[i]
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
        return self.youla_annoy.get_nns_by_vector(
            self.text2vec(text), number)

    def knn_hh(self, text, number=10):
        """
        Поиск похожих вакансий
        :param text: текст в виде строки
        :param number: число похожих объявлений
        :return: список номеров строк похожих объявлений в бд
        """
        return self.hh_annoy.get_nns_by_vector(
            self.text2vec(text), number)

    def _cosine_similarity(self, x, y):
        return np.dot(x, y) / (np.linalg.norm(x) *
                               np.linalg.norm(y))

    def knn_dummy(self, text):
        """
        Предсказывание хотелки пользователя
        :param text: текст в виде строки
        :return: youla, hh или dummy
        """
        text_vec = self.text2vec(text)
        youla_similar = list(map(
            lambda x: self._cosine_similarity(x, text_vec),
            self.youla_vectors))
        hh_similar = list(map(
            lambda x: self._cosine_similarity(x, text_vec),
            self.hh_vectors))
        if max(youla_similar) >= max(hh_similar):
            if max(youla_similar) >= CRITICAL_COSINE_SIMILARITY:
                return 'youla'
            else:
                return 'dummy'
        else:
            if max(hh_similar) >= CRITICAL_COSINE_SIMILARITY:
                return 'hh'
            else:
                return 'dummy'

    def _load_youla_annoy(self, youla_annoy_filename=None):
        """
        Загрузка векторов вещей
        :param youla_annoy_filename: название файла с векторами
        """
        if youla_annoy_filename is None:
            file_path = path.join(YOULA_ANNOY_FOLDER,
                                  listdir(YOULA_ANNOY_FOLDER)[-1])
        else:
            file_path = path.join(YOULA_ANNOY_FOLDER,
                                  youla_annoy_filename)
        self.youla_annoy = AnnoyIndex(300)
        self.youla_annoy.load(file_path)

    def _load_hh_annoy(self, hh_annoy_filename=None):
        """
        Загрузка векторов вакансий
        :param hh_annoy_filename: название файла с векторами
        """
        if hh_annoy_filename is None:
            file_path = path.join(HH_ANNOY_FOLDER,
                                  listdir(HH_ANNOY_FOLDER)[-1])
        else:
            file_path = path.join(HH_ANNOY_FOLDER,
                                  hh_annoy_filename)
        self.hh_annoy = AnnoyIndex(300)
        self.hh_annoy.load(file_path)

    def _load_categories_dict(self, categories_dict_filename=None):
        """
        Загрузка векторов вакансий
        :param categories_dict_filename: название файла со словарем
        """
        if categories_dict_filename is None:
            file_path = path.join(CATEGORIES_DICT_FOLDER,
                                  listdir(CATEGORIES_DICT_FOLDER)[-1])
        else:
            file_path = path.join(CATEGORIES_DICT_FOLDER,
                                  categories_dict_filename)
        with open(file_path, "rb") as f:
            self.categories_dict = load(f)

    def _load_knn_model(self, knn_model_filename=None):
        """
        Загрузка модели KNC
        :param knn_model_filename: название файла с моделью
        """
        if knn_model_filename is None:
            file_path = path.join(KNN_MODEL_FOLDER,
                                  listdir(KNN_MODEL_FOLDER)[-1])
        else:
            file_path = path.join(KNN_MODEL_FOLDER,
                                  knn_model_filename)
        with open(file_path, 'rb') as f:
            self.knn_model = load(f)

    def _load_w2v_model(self):
        """
        Загрузка Word2Vec
        """
        self.w2v_model = KeyedVectors.load(W2V_MODEL_FILE)

    def _load_dummy_vectors(self):
        """
        Загрузка решающих векторов
        """
        youla_vectors = ['одежда', 'обувь', 'вещь', 'устройство', 'телефон', 'запчасть']
        hh_vectors = ['работа', 'зарплата', 'опыт', 'стажировка', 'график', 'профессия']
        self.youla_vectors = list(map(lambda x: self.text2vec(x), youla_vectors))
        self.hh_vectors = list(map(lambda x: self.text2vec(x), hh_vectors))

    def _load_stopwords(self):
        """
        Загрузка стоп слов
        """
        with open(STOPWORDS_FILE, encoding="utf8") as f:
            self.stopwords = f.read().split()

    def wish_handler(self, text, number=10):
        """
        Обработка хотелки и выдача похожих результатов
        :param text: текст в виде строки
        :param number: число похожих результатов
        :return: тип хотелки, список номеров строк в бд
        """
        decision = self.knn_dummy(text)
        if decision == 'youla':
            return 'youla', self.knn_youla(text, number)
        elif decision == 'hh':
            return 'hh', self.knn_hh(text, number)
        else:
            return 'dummy', 'dummy'

    def predict(self, id):
        """
        Предсказание категории объявление
        :param id: уникальный номер объявления
        :return: category_id, category_name
        """
        data = pd.DataFrame(get_hh(id=id, fields=["title", "description"]))
        vec_text = self.text2vec(data['title'] + ' ' + data['description'])
        category_id = self.knn_model.predict([vec_text])[0]
        return category_id, self.categories_dict[category_id]


class DataDumper:
    """
    Сохранение данных с базы в локальные файлы для использования в Model
    """

    def __init__(self, model):
        self.model = model

    def dump(self, hh=False, youla=False, with_categories=False):
        """
        Вызов методов
        :param hh: сохранить данные с hh
        :param youla: сохранить данные с юлы
        :param with_categories: сохранить категории и переобучить предсказалку
        :return: тапл названий сохраненных файлов
        """
        hh_filename = ""
        if hh:
            hh_filename = self._dump_hh(with_categories=with_categories)
        youla_filename = ""
        if youla:
            youla_filename = self._dump_youla()
        return hh_filename, youla_filename

    def _dump_hh(self, with_categories=False):
        """
        Сохранение данных с базы hh
        :param with_categories: сохранить категории и переобучить предсказалку
        :return: тапл названий сохраненных файлов
        """
        hh_annoy = AnnoyIndex(300)
        categories_dict_filename = ""
        knn_model_filename = ""
        # data = pd.read_csv('.data/datasets/hh_dataset.csv')
        if with_categories:
            data = pd.DataFrame(get_hh(fields=["title", "description"],
                                       cats=["category_id", "category_name"]))
        else:
            data = pd.DataFrame(get_hh(fields=["title", "description"]))
        data.title.fillna('', inplace=True)
        data.description.fillna(data.title, inplace=True)
        data['text'] = data.title + ' ' + data.description
        vec = np.empty((data.shape[0], 300), dtype=np.float)
        for i in range(data.shape[0]):
            vec[i] = self.model.text2vec(data.iloc[i]['text'])
        if with_categories:
            knn_model = KNeighborsClassifier()
            knn_model.fit(vec, data['category_id'].values)
            knn_model_filename = "knn_model_" + \
                                 datetime.now().strftime('%Y%m%d%H%M%S') + \
                                 ".pkl"
            with open(path.join(KNN_MODEL_FOLDER, knn_model_filename), "wb") as f:
                dump(knn_model, f)
            cats = data.drop_duplicates(subset='category_id')
            categories_dict = dict()
            for i in cats[['category_id', 'category_name']].values:
                categories_dict[i[0]] = i[1]
            categories_dict_filename = "categories_dict_" + \
                                       datetime.now().strftime('%Y%m%d%H%M%S') + \
                                       ".pkl"
            with open(path.join(CATEGORIES_DICT_FOLDER, categories_dict_filename), "wb") as f:
                dump(categories_dict, f)
        for i, j in enumerate(vec):
            hh_annoy.add_item(data.iloc[i]['id'], j)
        hh_annoy.build(10)
        hh_annoy_filename = "hh_annoy_" + \
                            datetime.now().strftime('%Y%m%d%H%M%S') + \
                            ".ann"
        hh_annoy.save(path.join(HH_ANNOY_FOLDER, hh_annoy_filename))
        return hh_annoy_filename, categories_dict_filename, knn_model_filename

    def _dump_youla(self):
        """
        Сохранить данные с базы юлы
        :return: название сохраненного файла
        """
        youla_annoy = AnnoyIndex(300)
        # data = pd.read_csv('.data/datasets/youla_dataset.csv')
        data = pd.DataFrame(get_youla(fields=["title", "description"]))
        data.title.fillna('', inplace=True)
        data.description.fillna(data.title, inplace=True)
        data['text'] = data.title + ' ' + data.description
        vec = np.empty((data.shape[0], 300), dtype=np.float)
        for i in range(data.shape[0]):
            vec[i] = self.model.text2vec(data.iloc[i]['text'])
        for i, j in enumerate(vec):
            youla_annoy.add_item(data.iloc[i]['id'], j)
        youla_annoy.build(10)
        youla_annoy_filename = "youla_annoy_" + \
                               datetime.now().strftime('%Y%m%d%H%M%S') + \
                               ".ann"
        youla_annoy.save(path.join(YOULA_ANNOY_FOLDER, youla_annoy_filename))
        return youla_annoy_filename
