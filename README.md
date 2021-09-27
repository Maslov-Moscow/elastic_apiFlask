# elastic_apiFlask

API для поиска текста в базе данных. Поиск происходит в elasticsearch.

## Запуск
1. Замениете файл  *db.db* на файл *SQLite* c вашими данными либо оставте данный файл с тестовыми данными.
2. Выполните ```docker-compose up``` в корневой директории.
3. Документацию будет доступна [тут](http://localhost/swagger/). По умолчаню сервер принимает запросы *http://localhost/*

## Технологии
* Flask
* Elasticsearch
* Sqlite
* Docker
* NGINX
