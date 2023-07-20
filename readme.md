Этот проект является частью проекта для работы с адресами и служит хранилищем адресов, которые пользователи уже использовали в сервисе, чтобы не вызывать дополнительно api сторонних ресурсов.




deploy/configs/config.json

Переменные, которые отвечают за сервер базы данных и за поднятие API.

db_config

       user = "" - логин подключения к бд
       password = "" - пароль подключения к бд
       name = "" - название databases
       host = "" - хост бд
  
api

       password = "" - хешированный пароль для подключения к бд, в auth/auth.py лежат функции для его формирования

Каждый метод должен иметь в json-запросе строчку "password": "значение пароля", если он отсутствует (или неправильный) будет приходить ошибка 401 Unauthorized.

Имеется бд, в которой хранятся адреса с их координатами:

       'row_id': int
       'addr_init': str - изначальный адрес
       'addr_clean': str - "почищенная" строк адреса 
       'addr_dadata': str - адрес, полученный с помощью сервиса dadata
       'addr_yandex': str - адрес, полученный с помощью сервиса yandex
       'lat_dadata': float - широта, полученный с помощью сервиса dadata
       'lon_dadata': float - долгота, полученный с помощью сервиса dadata
       'aq_dadata': int, - погрешность, полученных данных с помощью сервиса dadata
       'lat_yandex': float - широта, полученный с помощью сервиса yandex
       'lon_yandex': float - долгота, полученный с помощью сервиса yandex

Метод GET:

	1). Запрос по row_id происходит по адресу "host:port/address/", json-файл типа {"row_id": int}. Ответ выглядит так:
	    {'row_id': int, 'addr_init': str, 'addr_clean': str, 'addr_dadata': str, 'addr_yandex': str, 'lat_dadata': float, 'lon_dadata': float, 'aq_dadata': int,
	    'lat_yandex': float, 'lon_yandex': float}
     
	2). Запрос по addr_ происходит по адресу "host:port/address/addr/", отправляется json-файл типа {"addr": значение, которое нужно найти}, обратно 
	    возвращается массив словарей из базы(в которых колонки addr_ равны отправленному "addr"). Вариант ответа:
	[{'row_id': 12, 'addr_init': 'Москва', 'addr_clean': 'NULL', 'addr_dadata': 'NULL', 'addr_yandex': 'Москва, ул. Ленина', 'lat_dadata': 'NULL', 'lon_dadata': 'NULL', 
	'aq_dadata':'NULL', 'lat_yandex': 'NULL', 'lon_yandex': 'NULL'}, {'row_id': 13, 'addr_init': 'Москва', 'addr_clean': 'NULL', 'addr_dadata': 'NULL', 'addr_yandex': 'NULL', 'lat_dadata': 'NULL',
 	'lon_dadata': 'NULL', 'aq_dadata': 'NULL', 'lat_yandex': 'NULL', 'lon_yandex': 'NULL'}, {'row_id': 14, 'addr_init': 'Москва', 'addr_clean': 'NULL', 'addr_dadata': 'NULL', 'addr_yandex': 'NULL',
  	'lat_dadata': 'NULL', 'lon_dadata': 'NULL', 'aq_dadata': 'NULL', 'lat_yandex': 'NULL', 'lon_yandex': 'NULL'}]
Метод POST:

	1). Запрос происходит по адресу "host:port/address/", json-файл должен иметь переменную ("addr_init": значение), а также может иметь любые дополнительные переменные 
	('addr_clean': str, 'addr_dadata': str, 'addr_yandex': str, 'lat_dadata': float, 'lon_dadata': float, 'aq_dadata': int, 'lat_yandex': float, 'lon_yandex': float), 
	при успешном запросе возвращаются данные в json, которые были занесены в базу.
 
Метод DELETE:

	1). Запрос происходит по адресу "host:port/address/", json-файл типа {"row_id": int}, при успешном запросе возвращается строка
	"The deletion was successful."
 
Метод PATCH:

	1). Запрос происходит по адресу "host:port/address/", json-файл должен иметь переменную ("row_id": int), а также может иметь любые дополнительные переменные 
	('addr_clean': str, 'addr_dadata': str, 'addr_yandex': str, 'lat_dadata': float, 'lon_dadata': float, 'aq_dadata': int, 'lat_yandex': float, 'lon_yandex': float),
	при успешном запросе возвращается строка 'Changes have been successfully applied'.

Для использования сваггера нужно зайти на на "host:port/docs/".
