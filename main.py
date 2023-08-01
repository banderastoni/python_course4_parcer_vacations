import json

from Classes.apiclasses import HeadHunterAPI, SuperJobAPI
from Classes.Vacancy import Vacancy
from Classes.json_funcs_class import JSONSaver, JSONLoader, save_to_json, JSONDeleter, JSONResponse, JSONSort


def user_interaction():
    platforms = ['1', '2', '3']
    platform = 0
    all_vacancies = []

    while platform not in platforms:
        resposibility_sj = 'см. в предыдущее поле'
        platform = input("Выберите платформу (1 или 2 или 3(все)):\n   1) HeadHunter\n   2) SuperJob\n   3) Все\n")
        match platform:
            case '1':
                print("Вы выбрали HeadHunter")

                # Создание экземпляра класса для работы с API сайтов с вакансиями
                hh_api = HeadHunterAPI()
                # Получение вакансий с разных платформ
                hh_vacancies = hh_api.get_vacancies("Python")

                for vacancy in hh_vacancies:
                    hh_vacancy = Vacancy(vacancy['name'], vacancy['salary']['from'], vacancy['salary']['to'],
                                         vacancy['alternate_url'],
                                         vacancy['snippet']['requirement'],
                                         vacancy['snippet']['responsibility'])
                    all_vacancies.append(hh_vacancy)
            case '2':
                print("Вы выбрали SuperJob")

                # Создание экземпляра класса для работы с API сайтов с вакансиями
                superjob_api = SuperJobAPI()
                # Получение вакансий с разных платформ
                superjob_vacancies = superjob_api.get_vacancies("Python")

                for vacancy in superjob_vacancies:
                    sj_vacancy = Vacancy(vacancy['profession'], vacancy['payment_from'], vacancy['payment_to'],
                                         vacancy['link'],
                                         vacancy['candidat'],
                                         None)
                    all_vacancies.append(sj_vacancy)
            case '3':
                print("Вы выбрали все платформы вакансий")

                # Создание экземпляра класса для работы с API сайтов с вакансиями
                hh_api = HeadHunterAPI()
                superjob_api = SuperJobAPI()
                # Получение вакансий с разных платформ
                hh_vacancies = hh_api.get_vacancies("Python")
                superjob_vacancies = superjob_api.get_vacancies("Python")

                for vacancy in hh_vacancies:
                    hh_vacancy = Vacancy(vacancy['name'], vacancy['salary']['from'], vacancy['salary']['to'],
                                         vacancy['alternate_url'],
                                         vacancy['snippet']['requirement'],
                                         vacancy['snippet']['responsibility'])
                    all_vacancies.append(hh_vacancy)

                for vacancy in superjob_vacancies:
                    sj_vacancy = Vacancy(vacancy['profession'], vacancy['payment_from'], vacancy['payment_to'],
                                         vacancy['link'],
                                         vacancy['candidat'],
                                         None)
                    all_vacancies.append(sj_vacancy)
            case _:
                print("Неправильный ввод. Попробуйте ещё раз.\n")

    # Сохраняю все вакансии в файл json
    save_to_json(all_vacancies, 'json/all_vacancies.json')
    json_saver = JSONSaver()
    # Фильтр вакансии по зарплате не менее чем
    min_salary = int(input("Введите минимальную зарплату:\n"))
    json_loader = JSONLoader()
    dict_vacancy_with_salary_filter = json_loader.get_vacancies_by_salary(min_salary, 'json/all_vacancies.json')
    # Записываю в файл json suitable_vacancies.json
    json_saver.add_vacancy(dict_vacancy_with_salary_filter, 'json/suitable_vacancies.json')

    # Сортировка вакансий по зарплате от меньшего к большему
    json_sort = JSONSort()
    json_sort.sort_vacancy('json/suitable_vacancies.json', 'json/suitable_vacancies_sorted.json')

    # Удаляю вакансию по ссылке
    json_deleter = JSONDeleter()
    json_deleter.delete_vacancy("https://hh.ru/vacancy/84302495", 'json/suitable_vacancies_del.json')

    # Поисковый запрос пользователя в описании вакансии
    response = input("Введите поисковый запрос:\n")
    json_response = JSONResponse()
    suitable_vacancies_by_response = json_response.get_vacancies_by_response(response,
                                                                             'json/suitable_vacancies_by_response.json')


if __name__ == "__main__":
    user_interaction()

    '''
    позволять пользователю:
    +1) указать, с каких платформ он хочет получить вакансии, 
    +2) ввести поисковый запрос, 
    3) получить топ N вакансий по зарплате,
    4) получить вакансии в отсортированном виде, 
    +5) получить вакансии, в описании которых есть определенные ключевые слова, например "postgres" и т. п.

    ## Требования к реализации в парадигме ООП

    +1. Абстрактный класс и классы для работы с API сайтов с вакансиями должны быть реализованы в соответствии с принципом
       наследования.
    +2. Класс для работы с вакансиями должен быть реализован в соответствии с принципом инкапсуляции и поддерживать методы
       сравнения вакансий между собой по зарплате.
    +3. Классы и другие сущности в проекте должны удовлетворять минимум первым двум требованиям принципов SOLID.
    '''
