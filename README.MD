
### Installation and Launch



1. First, you need to create a .env file in the assistant folder:
```
DEBUG_MODE=0
LLM_PROVIDER=YANDEX  // REPLICATE OR YANDEX
PG_HOST=<your db host>
PG_DBNAME=<your db name>
PG_PORT=<your db port>
PG_USER=<your db user>
PG_PASSWORD=<your db password>
YANDEX_API_KEY=<your yandex api-key>
YANDEX_FOLDER_ID=<your yandex folder id>
```

2. Then execute the commands in sequence:
```
make setup
source .venv/bin/activate
make run
```
