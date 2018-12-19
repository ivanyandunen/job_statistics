import requests
import os
from dotenv import load_dotenv
load_dotenv()
from terminaltables import AsciiTable


def get_number_of_vacancies(language):
    page = 0
    vacancies_list = []
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text':language,
        'area':'2', #Санкт-Петербург
        'period':'30',
        'page':page
    }
    pages = requests.get(url, params=params).json()['pages']

    for page in range(pages):
        for vacancy in requests.get(url, params=params).json()['items']:
            vacancies_list.append(vacancy)
    
    return len(vacancies_list)


def get_salary_by_language(language):
    page = 0
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text':'программист {}'.format(language),
        'area':'2', #Санкт-Петербург
        'period':'30',
        'only_with_salary':'true',
        'currency':'RUR',
        'page':page
    }
    pages = requests.get(url, params=params).json()['pages']
    
    for page in range(pages):
        for vacancy in requests.get(url, params=params).json()['items']:
            yield vacancy['salary']


def get_vacancies(token, language):
    page = 0
    list_of_vacancies = []
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': token}
    params = {
        'town':14, #Санкт-Петербург
        'keyword':'программист {}'.format(language),
        'currency':'rub',
        'page':page
    }
    pages = requests.get(url, headers=headers, params=params).json()['total']
    for page in range(pages):
        for vacancy in requests.get(
                url,
                headers=headers,
                params=params
            ).json()['objects']:
            list_of_vacancies.append(vacancy)
    return list_of_vacancies


def predict_rub_salary(payment_from, payment_to):
    if not payment_from and not payment_to:
        return None
    elif payment_from == None:
        return payment_to * 0.8
    elif payment_to == None:
        return payment_from * 1.2
    else:
        return (payment_from + payment_to) / 2
        
        
def get_average_salary(list_of_salaries):
    if not list_of_salaries:
        return None
    average_salary = 0
    for salary in list_of_salaries:
        if salary:
            average_salary += salary
    return int(average_salary / len(list_of_salaries))

    
def print_table(dict_of_vacancies, title):
    table_data = [
        [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
        ]
    ]
    for language in dict_of_vacancies:
        table_data.append((
            language,
            dict_of_vacancies[language]['vacancies_found'],
            dict_of_vacancies[language]['vacancies_processed'],
            dict_of_vacancies[language]['average_salary'])
        )
    table = AsciiTable(table_data, title)
    print(table.table)


def get_info_from_HH(dict_of_vacancies):
    for language in dict_of_vacancies.keys():
        salaries_by_language = []
        dict_of_vacancies[language]['vacancies_found'] = get_number_of_vacancies(language)
        for salary in get_salary_by_language(language):
            salaries_by_language.append(predict_rub_salary(
                salary['from'],
                salary['to'])
            )
        dict_of_vacancies[language]['vacancies_processed'] = len(salaries_by_language)
        dict_of_vacancies[language]['average_salary'] = get_average_salary(salaries_by_language)
    print_table(dict_of_vacancies, 'HeadHunter Saint-Petersburg')
    

def get_info_from_SJ(dict_of_vacancies):
    for language in dict_of_vacancies.keys():
        salaries_by_language = []
        list_of_vacancies = get_vacancies(token, language)
        dict_of_vacancies[language]['vacancies_found'] = len(list_of_vacancies)
        for vacancy in list_of_vacancies:
            salary = predict_rub_salary(
                    vacancy['payment_from'],
                    vacancy['payment_to']
                )
            if salary:
                salaries_by_language.append(salary)
        dict_of_vacancies[language]['vacancies_processed'] = len(salaries_by_language)
        dict_of_vacancies[language]['average_salary'] = get_average_salary(salaries_by_language)
    print_table(dict_of_vacancies, 'SuperJob Saint-Petersburg')

    
if __name__ == '__main__':
    dict_of_vacancies = {
        'JavaScript': {}, 
        'Java': {},
        'Python': {},
        'Ruby': {},
        'PHP': {},
        'C++': {},
        'C#': {},
        'C': {},
        'Go': {}
    }

    token = os.getenv('TOKEN')

    get_info_from_HH(dict_of_vacancies)
    get_info_from_SJ(dict_of_vacancies)
