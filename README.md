# Тестовое задание стажера в Avito Market Intelligence
JSON API сервис для отслеживания изменений в количестве объявлений на Авито по определенному поисковому запросу и региону на базе FastApi и MongoDb.
## Запуск сервиса
Перейти в директорию сборки, например:  
```cd EXAMPLE_DIR```  
Клонировать проект:  
```git clone https://github.com/Dukastlik/avito-statistic-trainee```  
Перейти в директорию avito-statistic-trainee:  
```cd avito-statistic-trainee```  
Запустить проект с помощью `docker-compose`:  
```docker-compose up```  
  
**Сервис доступен по http://0.0.0.0:8001**

  
## Интерфейс
1. Метод `add` добавляет пару запрос/регион в систему, чтобы воспользоваться методом нужно:  
Отправить по адресу http://0.0.0.0:8001/add `POST` запрос со словарем вида:
```
{
  "query": <query_name>
  "region": <region_name>
}
```  
Для тестирования можно воспользоваться файлом test_add.json из корневого каталога репозитория и curl:  
```curl -d @"test_add.json" -X POST http://0.0.0.0:8001/add```  
В ответ сервис пришлет словарь с id новой пары вида:  
```{'new_id": <new_pair_id>}```  
  
    
2. Метод `stat` присылает собранную статистику по количеству объявлений и словарь с 4мя самыми популярными объявлениями за временно промежуток, чтобы воспользоаться методом нужно:
Отправить по адресу http://0.0.0.0:8001/stat `GET` запрос со словарем вида:
```
{
  "id": <query-region-id>,
  "start_time": <datetime>,
  "end_time": <datetime>
}
```  
границы времнного промежутка ("start_time" и "end_time") передавать в формате: `YYYY-MM-DD-HH`  
Для тестирования можно воспользоваться файлом test_stat.json из корневого каталога репозитория и curl:  
```curl -d @"test_stat.json" -X GET http://0.0.0.0:8001/stat```  
В ответ сервис пришлет собранную статистику например:  
```
{"2020-12-13T22:48:36.063268":{  
"ad count":252324,  
"top ads":[  
{"ad_title":"1-к квартира, 39.8 м², 9/9 эт.","ad_uri":"https://www.avito.ru//moskva/kvartiry/1-k_kvartira_39.8_m_99_et._1997212090"},  
{"ad_title":"2-к квартира, 47.3 м², 4/21 эт.","ad_uri":"https://www.avito.ru//moskva/kvartiry/2-k_kvartira_47.3_m_421_et._2057440197"},  
{"ad_title":"3-к квартира, 84.8 м², 2/17 эт.","ad_uri":"https://www.avito.ru//moskva/kvartiry/3-k_kvartira_84.8_m_217_et._1961553320"},  
{"ad_title":"3-к квартира, 72.8 м², 24/25 эт.","ad_uri":"https://www.avito.ru//moskva/kvartiry/3-k_kvartira_72.8_m_2425_et._2019548981"}  
]}}  
```

### Кроме того  
- Сервис использует api Авито для получения статистики.  
- Сервис асинхронно обрабатывает запросы.  
- Вся статистика хранится в MongoDb.  
- Для обновления статистики используются fastapi.BackgroundTasks, что накладывает определенные ограничения на работу сервиса. Лучшей практикой было бы использование `celery` или `cron`. 
