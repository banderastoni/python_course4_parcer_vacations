import json

from Classes.apiclasses import HeadHunterAPI, SuperJobAPI
from Classes.Vacancy import Vacancy

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
superjob_api = SuperJobAPI()

# Получение вакансий с разных платформ
hh_vacancies = hh_api.get_vacancies("Python")
superjob_vacancies = superjob_api.get_vacancies("Python")


def user_interaction():
    platforms = ['1', '2']
    platform = 0
    all_vacancies = []

    while platform not in platforms:
        platform = input("Выберите платформу (1 или 2):\n   1) HeadHunter\n   2) SuperJob\n")
        print("Вы выбрали HeadHunter") if platform == '1' else 'Вы выбрали SuperJob'
        match platform:
            case '1':
                for vacancy in hh_vacancies:
                    hh_vacancy = Vacancy(vacancy['name'], vacancy['salary']['from'], vacancy['salary']['to'],
                                         vacancy['alternate_url'],
                                         vacancy['snippet'])
                    all_vacancies.append(hh_vacancy)
            case '2':
                for vacancy in superjob_vacancies:
                    sj_vacancy = Vacancy(vacancy['profession'], vacancy['payment_from'], vacancy['payment_to'],
                                         vacancy['link'],
                                         vacancy['candidat'])
                    all_vacancies.append(sj_vacancy)
            case _:
                print("Неправильный ввод. Попробуйте ещё раз.\n")

    vacs = []

    for vac in all_vacancies:
        vacs.append(vac.__dict__)

    with open('json/all_vacancies.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(vacs, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    user_interaction()
