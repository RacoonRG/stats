import requests
import pandas as pd
import os
from datetime import datetime, timedelta


def delete_sub(x: str):
    result = x.replace('/', "")
    result = result.replace('\\\\', '')
    result = result.replace('"', '')
    return result


print('@koff.ru =1')
print('@koff.ru =2')
print('@koff.ru =3')

user_input = input("Введите цифру соответсвующую вашему родительскому логину: ")
if user_input == '2':
    token = 'aa57809d0'
elif user_input == '3':
    token = '55b9638c3'
elif user_input == '1':
    token = '7a24f87c9'
else:
    token = 'Требуется ввести цифру от 1 до 3 и нажать Enter'
start_date = input('Введите дату начала выборки в формате (YYYY-MM-DD): ')
print('Дополнительный параметр - по умолчанию текущая дата')
end_date = input('Введите дату окончания выборки в формате (YYYY-MM-DD): ')
print('Дополнительный параметр')
user_id = input('Введите user id (опционально): ')
print('Дополнительный параметр - Позволяет получить данные о конкретном мероприятии.')
eventId = input("Введите Event id (опционально):")

ot = start_date
do = end_date
start_date2 = start_date
end_date2 = end_date
url = f'https://userapi.webinar.ru/v3/stats/events'
headers = {
    "x-auth-token": token,
    "content-type": "application/x-www-form-urlencoded"
}

result = []

current_date = start_date
start_date = datetime.strptime(start_date, '%Y-%m-%d')
end_date = datetime.strptime(end_date, '%Y-%m-%d')

while start_date <= end_date:
    start_time = start_date
    end_time = start_date
    start = (start_time.strftime('%Y-%m-%d') + 't00:00:00')
    end = (end_time.strftime('%Y-%m-%d') + 't23:59:59')
    params = {
        "from": start,
        "to": end,
        'user_id': user_id,
        'eventId': eventId
    }
    response = requests.get(url=url, params=params, headers=headers)

    json_data = response.json()
    result.extend(json_data)
    start_date += timedelta(days=1)

df = pd.DataFrame(result)
df.to_excel(f'Выборка мероприятий {ot}_{do}.xlsx')
os.makedirs('Статистика по участникам ', exist_ok=True)
for i in result:
    if type(i['referrer']) is list:
        continue
    else:
        link = list(i["referrer"].keys())[0].split(sep='/')
    if len(link) < 7:
        continue
    ev_id = link[4]
    url1 = 'https://userapi.webinar.ru/v3/stats/users'
    params2 = {
        'from': start_date2,
        'to': end_date2,
        'eventId': ev_id
    }
    response1 = requests.get(url=url1, params=params2, headers=headers)

    if response1.status_code in [404, 406]:
        # pd.DataFrame().to_excel(
        #   'Статистика по участникам' + "\\" + f'{"".join(map(delete_sub, i["name"]))}_{(i["startsAt"].split(sep="T"))[0]}.xlsx')
        # print(response1.status_code)
        continue
    else:
        print(response1.status_code)
        response1 = response1.json()

    for element in response1:
        element: dict
        element.update({'eventSessions': element['eventSessions'][0]})

    pd.DataFrame(response1).to_excel(
        'Статистика по участникам\\' + f'{"".join(map(delete_sub, i["name"]))}_{(i["startsAt"].split(sep="T"))[0]}.xlsx')


# def rename_columns(df):
#     columns_mapping = {
#         'id': 'userid',
#         'email': 'email',
#         'name': 'имя',
#         'secondName': 'фамилия',
#         'pattrname': 'отчество',
#         'duration': 'длительность',
#         'sex': 'пол',
#         'phone': 'телефон',
#         'organization': 'организация',
#         'position': 'должность'
#     }
#     df = df.rename(columns=columns_mapping)
#     return df
#
#
# # Путь к папке со статистикой
# folder_path = 'Статистика по участникам'
#
# # Получаем список всех файлов в папке
# file_list = os.listdir(folder_path)
#
# # Проходимся по каждому файлу и изменяем имя столбцов
# for file in file_list:
#     # Проверяем, что файл имеет расширение .xlsx
#     if file.endswith('.xlsx'):
#         # Полный путь к файлу
#         file_path = os.path.join(folder_path, file)
#
#         # Загружаем файл в датафрейм
#         df = pd.read_excel(file_path)
#
#         # Изменяем имя столбцов
#         df = rename_columns(df)
#
#         # Сохраняем измененный датафрейм обратно в файл
#         df.to_excel(file_path, index=False)