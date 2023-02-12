import datetime
import requests
from env import location_ids
from pprint import pprint
import locale


def get_months():
    today = datetime.date.today()
    monat1 = today.replace(month=(today.month) % 12+1)
    monat2 = today.replace(month=(today.month+1) % 12+1)

    # To Do Jahreswechsel prüfen ob nicht doch 01.2022 gewählt wird
    monate = [[today.month, today.year], [monat1.month, monat1.year], [monat2.month, monat2.year]]

    #DEBUG zum Testen
    monate = [[1, 2023], [2, 2023], [3, 2023]]
    return monate


def iterate_months():
    results = {}
    for month, year in get_months():
        results.update(get_vacancies_by_month(month, year, location_ids))

    return results

def get_vacancies_by_day(datum, locations):
    jsontext = {
        "locale": "de-DE", 
        "isLegacyTos": False,
        "date": {"date": datum}, 
        "vehicleServices": [{"id": 4007}], 
        "vehicleType": {"id": 44}, 
        "vics": []
    }

    for ort in locations:
        jsontext["vics"].append({"id": ort, "externalLocale": "de-DE", "distance": 1})

    result = requests.post(url="https://www.tuv.com/tos-pti-relaunch-2019/rest/ajax/getVacanciesByDay", json=jsontext)

    all_vacancies_by_day = result.json()
    timetables = all_vacancies_by_day["timetables"]
    for content in timetables:
        vic = content["vic"]
        time_range_vacancies = content["timeRangeVacancies"]
        for element in time_range_vacancies:
            if element["hasTimes"] == True:
                for timeslots in element["timeslots"]:
                   if timeslots["availableDates"]:
                       available_dates = timeslots["availableDates"]
                       available_time = available_dates[0]
                       yield available_time

        

def get_vacancies_by_month(month, year, locations):
    jsontext = {
        "locale": "de-DE", 
        "isLegacyTos": False,
        "filterMonth": month, 
        "filterYear": year,
        "vehicleServices": [{"id": 4007}], 
        "vehicleType": {"id": 44}, 
        "vics": []
    }

    for ort in locations:
        jsontext["vics"].append({"id": ort, "externalLocale": "de-DE", "distance": 1})
    
    result = requests.post(url="https://www.tuv.com/tos-pti-relaunch-2019/rest/ajax/getVacanciesByMonth", json=jsontext)
    all_vacancies = result.json()["vacancies"]
    vacancies_by_date = {}
    for date in all_vacancies:
        vacancies_for_date = list(get_vacancies_by_day(date["date"], locations))
        if vacancies_for_date:
            vacancies_by_date[date["date"]] = vacancies_for_date

            ### Bookmark: vacancies_by_date Dict erstellt, muss noch zurück gegeben werden,
            # dann die Datenverarbeitung und Email Logik

    #pprint(vacancies_by_date)
    return vacancies_by_date


def format_date(dictionary):
    correct_format = {}
    for datum in dictionary:
        datum_correct_fomat = datetime.datetime.strptime(datum, '%Y-%m-%d').strftime('%a, %d.%m.%y')
        
        # Name neues Dict  # Schlüssel  # Wert
        # müssen zu dem neuen Dict zusammengefügt werden, was anschließend sortiert werden kann
        # correct_format       datum       dictionary[datum]


def gen_mail_general_overview(vacancies):
    for datum in vacancies:
        print(datum + ": " + ", ".join(vacancies[datum]))

        # Mailtext muss generiert werden

def send_mail():
    # schalalalalala
    print("bla")


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
    all_vacancies = iterate_months()
    format_date(all_vacancies)
    gen_mail_general_overview(all_vacancies)
