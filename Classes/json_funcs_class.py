import operator
import json
from abc import ABC, abstractmethod
from datetime import datetime

from Classes.Vacancy import Vacancy


class AbstractVacancy(ABC):
    """
    Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях.
    """

    @abstractmethod
    def add_vacancy(self, vacancy, filename):
        pass

    def get_vacancies_by_salary(self, salary, filename):
        pass

    def get_vacancies_by_response(self, response, filename):
        pass

    def delete_vacancy(self, vacancy_del, filename):
        pass

    def sort_vacancy(self, filename_from, filename_to):
        pass

    def read_file(self, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            data = json.load(f)
        return data

    def save_json(self, list_vacancy, file_name):
        pass


class JSONSaver(AbstractVacancy):
    """
    Класс для сохранения информации о вакансиях в JSON-файл.
    """

    def add_vacancy(self, vacancy, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(vacancy, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(vacancy)} вакансий в файл {filename}')

    def add_vacancies(self, vacancy, vacancy2, filename):
        new_list = []
        for item in vacancy:
            new_list.append(item.__dict__)
        for item in vacancy2:
            new_list.append(item.__dict__)
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(new_list, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(new_list)} вакансий.\n')

    def save_json(self, list_vacancy, file_name):
        new_list = []
        for item in list_vacancy:
            new_list.append(item.__dict__)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_list, indent=4, ensure_ascii=False))
        print(f'\n {len(new_list)} вакансий по вашему запросу сохранены в JSON-файл {file_name}.')


class JSONLoader(AbstractVacancy):
    """
    Класс для загрузки информации о вакансиях из JSON-файл.
    """

    def add_vacancy(self, vacancy, filename):
        pass

    def get_vacancies_by_salary(self, salary, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            data = json.load(f)
        new_list = []
        for item in data:
            if item['salary_from'] is None:
                continue
            if salary <= item['salary_from']:
                new_list.append(item)
        return new_list


class JSONDeleter(AbstractVacancy):
    """
    Класс для удаления определенной вакансии из JSON-файл.
    """

    def add_vacancy(self, vacancy, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(vacancy, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(vacancy)} вакансий в файл {filename} без лишней вакансии')

    def delete_vacancy(self, vacancy_del_url, filename):
        vacancies = []
        for vacancy in self.read_file('json/suitable_vacancies.json'):
            if vacancy['url'] != vacancy_del_url:
                vacancies.append(vacancy)
        self.add_vacancy(vacancies, filename)


class JSONResponse(AbstractVacancy):

    def add_vacancy(self, vacancy, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(vacancy, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(vacancy)} вакансий в файл {filename} соответствующих запросу')

    def get_vacancies_by_response(self, response, filename):
        vacancies = []
        for vacancy in self.read_file('json/suitable_vacancies.json'):
            if response in str(vacancy['info']) or response in str(vacancy['name']):
                vacancies.append(vacancy)
        self.add_vacancy(vacancies, filename)


class JSONSort(AbstractVacancy):
    def add_vacancy(self, vacancy, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(vacancy, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(vacancy)} вакансий в файл {filename} соответствующих запросу')

    def sort_vacancy_by_date(self, list_vacancies):
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

