from abc import ABC, abstractmethod

import json
from Classes.Vacancy import Vacancy


def save_to_json(vacancy, filename):
    vacs = []
    for item in vacancy:
        vacs.append(item.__dict__)
    with open(filename, 'w', encoding='UTF-8') as f:
        f.write(json.dumps(vacs, indent=2, ensure_ascii=False))
    print(f'\nЗаписано {len(vacs)} вакансий в файл {filename}\n')


def write_file(filename):
    pass


class AbstractVacancy(ABC):
    """
    Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях.
    """

    @abstractmethod
    def add_vacancy(self, vacancy, filename):
        pass

    def read_file(self, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            data = json.load(f)
        return data

    def get_vacancies_by_salary(self, salary, filename):
        pass

    def get_vacancies_by_response(self, response, filename):
        pass

    def delete_vacancy(self, vacancy_del, filename):
        pass

    def sort_vacancy(self, filename_from, filename_to):
        pass


class JSONSaver(AbstractVacancy):
    """
    Класс для сохранения информации о вакансиях в JSON-файл.
    """

    def add_vacancy(self, vacancy, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(vacancy, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(vacancy)} вакансий в файл {filename}')


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

    def sort_vacancy(self, filename_from, filename_to):
        # vacancies = sorted(filename_from, key=lambda d: d['salary_from'])
        vacancies_not_sorted = []
        vacancies_not_sorted = self.read_file(filename_from)
        vacancies_sorted = []
        vacancies_list = []
        counter = 0

        for vacancy in vacancies_not_sorted:
            vacancy_ = Vacancy(vacancy['name'],
                               vacancy['salary_from'],
                               vacancy['salary_to'],
                               vacancy['url'],
                               vacancy['info'],
                               vacancy['responsibility'])

            vacancies_list.append(vacancy_)
            counter += 1

            if vacancy_.__lt__(vacancies_list[counter - 1]):
                vacancies_sorted.append(vacancies_list[counter - 1])
                vacancies_sorted.append(vacancies_list[counter])
            print(vacancies_sorted)

        # vacancies_sorted = sorted(vacancies_list, key=lambda x: x['salary_from'], reverse=True)
        self.add_vacancy(vacancies_sorted, filename_to)
