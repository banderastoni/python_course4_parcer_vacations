import operator
from datetime import datetime

from Classes.Vacancy import Vacancy


def hh_for_list(hh_vacancies):
    hh_vacancies_list = []
    for vacancy in hh_vacancies:
        hh_vacancy = Vacancy(vacancy['name'],
                             vacancy['salary']['from'],
                             vacancy['salary']['to'],
                             vacancy['alternate_url'],
                             vacancy['snippet']['requirement'],
                             vacancy['snippet']['responsibility'],
                             vacancy["published_at"])
        hh_vacancies_list.append(hh_vacancy)
    return hh_vacancies_list


def sj_for_list(sj_vacancies):
    sj_vacancies_list = []
    for vacancy in sj_vacancies:
        sj_vacancy = Vacancy(vacancy['profession'],
                             vacancy['payment_from'],
                             vacancy['payment_to'],
                             vacancy['link'],
                             vacancy['candidat'],
                             None,
                             vacancy["date_published"])
        sj_vacancies_list.append(sj_vacancy)
    return sj_vacancies_list


def sorted_data(list_vacancies):
    """
    Сортируем по дате список вакансий.
    """
    for item in list_vacancies:
        if 'superjob.ru' in item['url']:
            item['published_at'] = datetime.fromtimestamp(item['published_at'])
            item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
            item['published_at'] = datetime.strptime(item['published_at'], '%d-%m-%Y %H:%M:%S')
        else:
            item['published_at'] = datetime.fromisoformat(item['published_at'])
            item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
            item['published_at'] = datetime.strptime(item['published_at'], '%d-%m-%Y %H:%M:%S')
    sorted_list = sorted(list_vacancies, key=operator.itemgetter('published_at'), reverse=True)
    for item in sorted_list:
        item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
    return sorted_list


def instance_vacancy_sorted(data):
    """
    Создаем список экземпляров класса, полученные после всех сортировок и фильтров.
    """
    vacancy_list = []
    for item in data:
        vacancy = Vacancy(item["name"],
                          item["salary_from"],
                          item["salary_to"],
                          item["url"],
                          item["info"],
                          item["responsibility"],
                          item["published_at"])
        vacancy_list.append(vacancy)
    return vacancy_list


def top_n_vacancies(list_vacancies, n):
    """
    Выводим top N вакансий.
    """
    list_top = []
    counter = 1
    for item in list_vacancies:
        print(item)
        list_top.append(item)
        counter += 1
        if counter > n:
            break
    return list_top
