DWH Assistant - это внутренний сервис, который может понимать вопросы пользователей на естественном языке и автоматически формировать SQL-запросы к историческим данным. Общий принцип работы DWH Assistant:

1. Пользователь формулирует свой вопрос на естественном языке. 
2. DWH Assistant, подготавливает prompt-инструкцию для LLM сформировать подходящий SQL-запрос, в который включает вопрос пользователя и DBML (схему таблиц базы данных).
3. Сформированную prompt-инструкцию приложение отправляет в LLM. Полученный от LLM ответ содержит SQL-запрос.
4. Приложение отправляет SQL-запрос на выполнение в базу данных.
5. Результат запроса показывается пользователю в виде таблицы.



### Установка и запуск



1. Создайте файл .env в папке проекта и добавьте следующие переменные:
```
DEBUG_MODE=0
LLM_PROVIDER=YANDEX
PG_HOST=<your db host>
PG_DBNAME=<your db name>
PG_PORT=<your db port>
PG_USER=<your db user>
PG_PASSWORD=<your db password>
YANDEX_API_KEY=<your yandex api-key>
YANDEX_FOLDER_ID=<your yandex folder id>
```

2. Выполните следующие команды:
```
make setup
source .venv/bin/activate
make run
```
