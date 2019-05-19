
# Gunicorn project. ML

## Что умеет модель
Модель умеет предсказывать тип хотелки, введенной пользователем (юла, hh, ни то ни другое), далее по этому типу искать похожие объявления на соответствующей платформе.

Еще модель умеет предсказывать категорию для вакансии. Это не изюминка проекта, сделана для того чтобы а почему бы и нет.


```python
%%time
import ml
model=ml.Model()
```

    Wall time: 1min 14s
    

## Что за данные
Данные лежат в базе, в ноутбуке используется локальная копия (не уверен) для улучшения производительности.


```python
%%time
import pandas as pd
data_hh=pd.read_csv(".data/hh_dataset.csv")
data_youla=pd.read_csv(".data/youla_dataset.csv")
```

    Wall time: 1.06 s
    


```python
data_hh.sample(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>title</th>
      <th>category_id</th>
      <th>category_name</th>
      <th>employer</th>
      <th>description</th>
      <th>salary_from</th>
      <th>salary_to</th>
      <th>currency</th>
      <th>metro_station</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>9405</th>
      <td>31371325</td>
      <td>Юрист</td>
      <td>23</td>
      <td>Юристы</td>
      <td>НТО Центр промышленной безопасности</td>
      <td>ДЛЯ КОГО ЭТА ВАКАНСИЯ Мы ищем юриста, который ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Волгоградский проспект</td>
    </tr>
  </tbody>
</table>
</div>




```python
data_youla.sample(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>title</th>
      <th>description</th>
      <th>product_id</th>
      <th>category_id</th>
      <th>subcategory_id</th>
      <th>properties</th>
      <th>image_links</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6523</th>
      <td>6523</td>
      <td>Зимняя куртка кожанная</td>
      <td>Кожанка зимняя 54_56</td>
      <td>5bb1d3fe0fff81421a6608d1</td>
      <td>8.0</td>
      <td>803</td>
      <td>{'muzhskaya_odezhda_verhnyaya_tip': 'Кожаные к...</td>
      <td>http://cache3.youla.io/files/images/360_360/5b...</td>
    </tr>
  </tbody>
</table>
</div>



## Поиск по юле
Для обучения использовался ансамбль BaggingClassifier на решающих деревьях. Векторизовались только названия объявлений, так как длинные описания усредняли вектор. Токенизация слов при помощи pymorphy2. Корпус слов для Word2Vec - Araneum, размерность вектора 300, алгоритм скипграм, обучен на 10млрд слов из [замечательного источника](https://www.google.ru/), взят [отсюда](https://rusvectores.org/static/models/rusvectores4/araneum/araneum_upos_skipgram_300_2_2018.vec.gz)


```python
text="синяя куртка для девочки с капюшоном"
ids=model.knn_youla(text, 5)
data_youla.iloc[ids][['title','description']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>23133</th>
      <td>Куртка подростковая для девочки р.40-42</td>
      <td>Куртка подростковая на девочку р.40-42. С капю...</td>
    </tr>
    <tr>
      <th>5187</th>
      <td>Куртка зимняя "MTFORCE"</td>
      <td>Зимняя куртка для девочки.</td>
    </tr>
    <tr>
      <th>6861</th>
      <td>Куртка джинсовая</td>
      <td>Модная курточка , на девочку .</td>
    </tr>
    <tr>
      <th>8909</th>
      <td>Куртка джинсовая</td>
      <td>Продам джинсовую курточку на девочку.</td>
    </tr>
    <tr>
      <th>35000</th>
      <td>Куртка зимняя для девочки</td>
      <td>Куртка зимняя для девочки. Подкладка- флис. Бе...</td>
    </tr>
  </tbody>
</table>
</div>



## Поиск по hh
Аналогично поиску по юле.


```python
text="водитель автобуса"
ids=model.knn_hh(text, 5)
data_hh.iloc[ids][['title','description']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6329</th>
      <td>Водитель категории Д на автобус</td>
      <td>В транспортную компанию на постоянную работу т...</td>
    </tr>
    <tr>
      <th>6192</th>
      <td>Водитель-дальнобойщик</td>
      <td>На постоянную работу требуется водитель-дально...</td>
    </tr>
    <tr>
      <th>16020</th>
      <td>Водитель такси Ford Focus</td>
      <td>Крупной транспортной компании требуются води...</td>
    </tr>
    <tr>
      <th>11685</th>
      <td>Водитель-курьер с личным автомобилем</td>
      <td>Обязанности:  сбор и доставка почтовых отправл...</td>
    </tr>
    <tr>
      <th>11706</th>
      <td>Водитель Яндекс такси на зарплату</td>
      <td>В штат на зарплату. Водитель Такси, НОВЫЕ АВТО...</td>
    </tr>
  </tbody>
</table>
</div>



## Определение типа хотелки
KNeighborsClassifier обучен на случайной 10 тыс. выборке с юлы и hh. Если максимальное значение не превышает критического, возвращается dummy-тип. Для ясности, печатаются вероятности принадлежности к hh и юле.


```python
text="безумно дорогая и ненужная вещь"
print(model.wish_detector(text))
```

    [0. 1.]
    youla
    


```python
text="Фронтенд программист без опыта"
print(model.wish_detector(text))
```

    [1. 0.]
    hh
    


```python
text="фигня которую не определить"
print(model.wish_detector(text))
```

    [0.4 0.6]
    dummy
    

**ЗЫ** однако фигни на юле больше чем на hh

## Классификация вакансий
Снова бэггинг решающих деревьев, снова на рандомной 10тыс. выборке


```python
text="Менеджер по продажам юридических услуг"
print(model.predict_text(text))
```

    (17, 'Продажи')
    


```python
data_hh.iloc[2656][['title','category_id','category_name']]
```




    title            Менеджер по продажам юридических услуг
    category_id                                           5
    category_name                 Банки, инвестиции, лизинг
    Name: 2656, dtype: object



по-моему, логичное предсказание

## Дамп данных
а именно:
* датасет юлы → анной + модель хотелки
* датасет hh → анной + модель хотелки
* категории hh → словарь + модель категории


```python
%%time
ml.dump_all()
```

    Wall time: 3min 46s
    

## Всё!
Оценки моделей лежат в [/model/ml2.ipynb](./ml2.ipynb)
