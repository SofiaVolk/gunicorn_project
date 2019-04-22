import requests
import re
import random
from bs4 import BeautifulSoup


def hh_url_constructor(specialisation_id):
    urls = []
    n_page = 3
    n_spec = 5
    for spec_id in random.sample(specialisation_id, n_spec):
        for page in range(n_page):
            url = 'https://api.hh.ru/vacancies?page=' + str(page) + '&area=1&specialization=' + spec_id  # per_page=20&
            urls.append(url)
    return urls


def hh_parsing():
    vacancy_id = []
    vacancy_name = []
    vacancy_spec = []
    # vacancy_employer_id = []
    vacancy_employer = []
    vacancy_salary_from = []
    vacancy_salary_to = []
    vacancy_currency = []
    vacancy_metro_station = []
    vacancy_address = []
    headers = {'User-Agent': 'api-test'}
    url_dict = {'all': "https://api.hh.ru/dictionaries", 'areas': "https://api.hh.ru/areas",
                'metro': "https://api.hh.ru/metro", 'specialisations': "https://api.hh.ru/specializations"}

    r_dict = requests.get(url_dict['all'], headers=headers)
    r_dict_areas = requests.get(url_dict['areas'], headers=headers)
    r_dict_metro = requests.get(url_dict['metro'], headers=headers)
    r_dict_spec = requests.get(url_dict['specialisations'], headers=headers)

    schedule_dict = {item['id']: item['name'] for item in r_dict.json()['schedule']}
    currency_dict = {item['code']: item['name'] for item in r_dict.json()['currency']}
    areas_dict = {int(area['id']): area['name'] for item in r_dict_areas.json() if item['name'] == 'Россия'
                  for area in item['areas'] if area['name'] == 'Москва'}
    metro_dict = {float(station['id']): station['name'] for item in r_dict_metro.json() if item['name'] == 'Москва'
                  for line in item['lines'] for station in line['stations']}
    specializations_dict = r_dict_spec.json()

    prof_area_id = [prof_area['id'] for item in specializations_dict for prof_area in item['specializations']]
    urls = hh_url_constructor(prof_area_id)

    for url in urls:
        r = requests.get(url, headers=headers)

        for vacancy in r.json()['items']:
            vacancy_id.append(int(vacancy['id']))
            vacancy_name.append(vacancy['name'])
            vacancy_spec.append(url.split('=')[-1])
            # vacancy_employer_id.append(int(vacancy['employer']['id']))
            vacancy_employer.append(vacancy['employer']['name'])

            if vacancy['salary'] is not None:
                vacancy_salary_from.append(vacancy['salary']['from'])
                vacancy_salary_to.append(vacancy['salary']['to'])
                vacancy_currency.append(vacancy['salary']['currency'])
            else:
                vacancy_salary_from.append(None)
                vacancy_salary_to.append(None)
                vacancy_currency.append(None)

            vacancy_address.append(vacancy['area']['name'])
            if vacancy['address'] is not None:
                if vacancy['address']['street'] is not None:
                    vacancy_address[len(vacancy_address)-1] = vacancy_address[len(vacancy_address)-1]+', '+vacancy['address']['street']
                    if vacancy['address']['building'] is not None:
                        vacancy_address[len(vacancy_address)-1] = vacancy_address[len(vacancy_address)-1]+', '+vacancy['address']['building']
                elif vacancy['address']['raw'] is not None:
                    vacancy_address[len(vacancy_address)-1] = vacancy_address[len(vacancy_address)-1]+', '+vacancy['address']['raw']
                if vacancy['address']['metro'] is not None:
                    vacancy_metro_station.append(vacancy['address']['metro']['station_name'])
                else:
                    vacancy_metro_station.append(None)
            else:
                vacancy_metro_station.append(None)

    print(len(vacancy_id))
    print(vacancy_name)
    print(vacancy_spec)
    # print(vacancy_employer_id)
    print(vacancy_employer)
    print(vacancy_salary_from)
    print(vacancy_salary_to)
    print(vacancy_currency)
    print(vacancy_metro_station)
    print(vacancy_address)
    return r.status_code


def cian_url_constructor():
    urls = []
    n_page = 10
    for page in range(n_page):
        url = "https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=1&p=" + str(page)
        urls.append(url)
    return urls


def cian_parsing():
    flat_id = []
    # flat_floor = []
    flat_rooms = []
    # flat_address = []
    flat_metro_station = []
    flat_price = []
    flat_price_per_meter = []
    flat_type = ['1-комн.', '2-комн.', '3-комн.', '4-комн.', '5-комн.', '6-комн.',
                 'Студия', 'Апартаменты-студия', 'Своб. планировка']

    urls = cian_url_constructor()
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        s = soup.find_all('div', attrs={"class": re.compile("--info--")})
        for i in enumerate(s):
            flat_id.append(int(i[1].find('a')['href'].split('/')[-2]))
            # flat_floor.append(int(i[1].get_text().split(' этаж')[0].split(', ')[-1].split('/')[0]))
            # flat_address.append(i[1].find('span')['content'])
            # flat_rooms.append(str([j for j in flat_type if j in i[1].get_text()]))
            for j in flat_type:
                if j in i[1].get_text():
                    flat_rooms.append(j)
                    break

        s = soup.find_all('div', attrs={"class": re.compile("--underground-name--")})
        for i in enumerate(s):
            flat_metro_station.append(i[1].get_text())

        s = soup.find_all('div', attrs={"class": re.compile("--price_flex_container--")})
        for i in enumerate(s):
            flat_price.append(int(i[1].get_text().split(' ₽')[0].replace(' ', '')))
            flat_price_per_meter.append(int(i[1].get_text().split(' ₽')[-2].replace(' ', '')))

    print(len(flat_id))
    print(flat_id)
    # print(flat_floor)
    print(flat_rooms)
    # print(flat_address)
    print(flat_metro_station)
    print(flat_price)
    print(flat_price_per_meter)
    return r.status_code


cian_parsing()
hh_parsing()
