import requests
import re
import random

HH_BASEURL = 'https://api.hh.ru'
PAGENUM = 10
SPECNUM = 10


def hh_url_constructor(specialisation_id):
    urls = []
    for spec_id in random.sample(specialisation_id, SPECNUM):
        for page in range(PAGENUM):
            url = f'{HH_BASEURL}/vacancies?page={page}&area=1&specialization={spec_id}'
            r = requests.get(url)

            for _ in r.json()['items']:
                urls.append(f'{HH_BASEURL}/vacancies/' + _['id'])
    return urls


def hh_parsing():
    r_dict = requests.get(f'{HH_BASEURL}/dictionaries')
    r_dict_metro = requests.get(f'{HH_BASEURL}/metro')
    r_dict_spec = requests.get(f'{HH_BASEURL}/specializations')

    currency_dict = {item['code']: item['name'] for item in r_dict.json()['currency']}
    metro_dict = {float(station['id']): station['name'] for item in r_dict_metro.json() if item['name'] == 'Москва'
                  for line in item['lines'] for station in line['stations']}
    specializations_dict = r_dict_spec.json()

    prof_area_id = [prof_area['id'] for item in specializations_dict for prof_area in item['specializations']]
    urls = hh_url_constructor(prof_area_id)

    for url in urls:
        r = requests.get(url)

        v = r.json()
        vacancy_db_format = [int(v['id']), v['name'], int(v['specializations'][0]['profarea_id']),
                             v['specializations'][0]['profarea_name'], v['employer']['name'],
                             re.sub(r'</?\w+/?>', '', v['description'])]

        if v['salary'] is not None:
            vacancy_db_format += v['salary']['from'], v['salary']['from'], v['salary']['currency']
        else:
            vacancy_db_format += None, None, None

        if v['address'] is not None and v['address']['metro'] is not None:
                vacancy_db_format.append(v['address']['metro']['station_name'])
        else:
            vacancy_db_format.append(None)
        print(vacancy_db_format)
    return r.status_code


hh_parsing()
