from numpy import zeros
from pymorphy2 import MorphAnalyzer
from re import findall
from functools import lru_cache
from gensim.models import KeyedVectors
from annoy import AnnoyIndex
import pandas as pd
from os import path

STOPWORDS_LOCAL = path.join(".datasets/stopwords.txt")
W2V_LOCAL = path.join(".araneum/araneum_none_fasttextskipgram_300_5_2018.model")
YOULA_LOCAL = path.join(".ann/youla.ann")
HH_LOCAL = path.join(".ann/hh.ann")
DUMMY_LOCAL = path.join(".ann/dummy.ann")


class Model:

    def __init__(self, stop_path=STOPWORDS_LOCAL, w2v_path=W2V_LOCAL,
                 youla_path=YOULA_LOCAL, hh_path=HH_LOCAL, dummy_path=DUMMY_LOCAL):
        '''
        :param stop_path: путь к файлу стоп слов
        :param w2v_path: путь к файлу Word2Vec
        :param youla_path: путь к файлу вещей
        :param hh_path: путь к фалу вакансий
        :param dummy_path: путь к решающему файлу
        '''
        self.morph = MorphAnalyzer()
        self.stopwords = None
        self.youla_annoy = None
        self.hh_annoy = None
        self.w2v = None
        self.dummy_annoy = None
        self._load_stopwords(stop_path)
        self._load_w2v(w2v_path)
        self._load_youla_annoy(youla_path)
        self._load_hh_annoy(hh_path)
        self._load_dummy_annoy(dummy_path)

    @lru_cache(maxsize=10000)
    def get_normal_form(self, word):
        '''
        Получение нормальной формы слова
        :param word: слово в виде строки
        :return: нормальная форма от pymorpy2
        '''
        return self.morph.normal_forms(word)[0]

    def text2vec(self, text):
        '''
        Векторизация текста
        :param text: текст в виде строки
        :return: вектор слова от Word2Vec
        '''
        words = [self.get_normal_form(i) for i in findall('\w+', text)
                 if ((not i.isdigit()) and (len(i) > 2) and
                     (i not in self.stopwords))]
        result = zeros(self.w2v.vector_size)
        for i in words:
            try:
                result += self.w2v[i]
            except KeyError:
                pass
        return result

    def youla_to_annoy(self, method='remote', path_from=None, path_to=YOULA_LOCAL):
        '''
        Сохранение векторов вещей
        :param method: метод получения данных: local или remote
        :param path_from: путь к файлу для local метода
        :param path_to: путь для сохранения векторов
        '''
        if method == 'remote':
            raise NotImplementedError
        else:
            data = pd.read_csv(path_from)
        data.title.fillna('', inplace=True)
        data.descrirption.fillna(data.title, inplace=True)
        data['text'] = data.title + ' ' + data.descrirption
        vec = data.text.apply(
            lambda x: self.text2vec(x)).values
        ann = AnnoyIndex(300)
        for i, j in enumerate(vec):
            ann.add_item(i, j)
        ann.build(10)
        ann.save(path_to)

    def hh_to_annoy(self, method='remote', path_from=None, path_to=HH_LOCAL):
        '''
        Сохранение векторов вакансий
        :param method: метод получения данных: local или remote
        :param path_from: путь к файлу для local метода
        :param path_to: путь для сохранения векторов
        '''
        if method == 'remote':
            raise NotImplementedError
        else:
            data = pd.read_csv(path_from)
        data.name.fillna('', inplace=True)
        data.description.fillna(data.name, inplace=True)
        data['text'] = data.name + ' ' + data.description
        vec = data.text.apply(
            lambda x: self.text2vec(x)).values
        ann = AnnoyIndex(300)
        for i, j in enumerate(vec):
            ann.add_item(i, j)
        ann.build(10)
        ann.save(path_to)

    def dummy_to_annoy(self, path_to=DUMMY_LOCAL):
        '''
        Сохранение решающих векторов
        :param path_to: путь для сохранения векторов
        '''
        youla_tags = 'одежда обувь машина телефон запчасть вещь'
        hh_tags = 'работа стажировка зарплата учеба график опыт'
        youla_vec = self.text2vec(youla_tags)
        hh_vec = self.text2vec((hh_tags))
        ann = AnnoyIndex(300)
        ann.add_item(0, youla_vec)
        ann.add_item(1, hh_vec)
        ann.build(1)
        ann.save(path_to)

    def knn_youla(self, text, number=10):
        '''
        Поиск похожих вещей
        :param text: текст в виде строки
        :param number: число похожих объявлений
        :return: список номеров строк похожих объявлений в бд
        '''
        return self.youla_annoy.get_nns_by_vector(
            self.text2vec(text), number)

    def knn_hh(self, text, number=10):
        '''
        Поиск похожих вакансий
        :param text: текст в виде строки
        :param number: число похожих объявлений
        :return: список номеров строк похожих объявлений в бд
        '''
        return self.hh_annoy.get_nns_by_vector(
            self.text2vec(text), number)

    def knn_dummy(self, text):
        '''
        Предсказывание хотелки пользователя
        :param text: текст в виде строки
        :return: youla или hh
        '''
        return 'youla' if self.dummy_annoy.get_nns_by_vector(
            self.text2vec(text), 1)[0] == 0 else 'hh'

    def _load_youla_annoy(self, path_from=YOULA_LOCAL):
        '''
        Загрузка векторов вещей
        :param path_from: путь файла с векторами
        '''
        if self.youla_annoy is not None:
            self.youla_annoy.unload()
        self.youla_annoy = AnnoyIndex(300)
        self.youla_annoy.load(path_from)

    def _load_hh_annoy(self, path_from=HH_LOCAL):
        '''
        Загрузка векторов вакансий
        :param path_from: путь файла с векторами
        '''
        if self.hh_annoy is not None:
            self.hh_annoy.unload()
        self.hh_annoy = AnnoyIndex(300)
        self.hh_annoy.load(path_from)

    def _load_dummy_annoy(self, path_from=DUMMY_LOCAL):
        '''
        Загрузка решающих векторов
        :param path_from: путь файла с векторами
        '''
        if self.dummy_annoy is not None:
            self.dummy_annoy.unload()
        self.dummy_annoy = AnnoyIndex(300)
        self.dummy_annoy.load(path_from)

    def _load_stopwords(self, path_from=STOPWORDS_LOCAL):
        '''
        Загрузка стоп слов
        :param path_from: путь файла со словами
        '''
        with open(path_from, encoding="utf8") as f:
            self.stopwords = f.read().split()

    def _load_w2v(self, path_from=W2V_LOCAL):
        '''
        Загрузка Word2Vec
        :param path_from: путь файла
        '''
        self.w2v = KeyedVectors.load(path_from)

    def wish_handler(self, text, number=10):
        '''
        Обработка хотелки и выдача похожих результатов
        :param text: текст в виде строки
        :param number: число похожих результатов
        :return: тип хотелки, список номеров строк в бд
        '''
        if self.knn_dummy(text) == 'youla':
            return 'youla', self.knn_youla(text, number)
        else:
            return 'hh', self.knn_hh(text, number)
