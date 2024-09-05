
### Installation and Launch



1. First, you need to create a .env file in the assistant folder:
```
DEBUG_MODE=0
LLM_PROVIDER=YANDEX  // REPLICATE OR YANDEX
CH_HOST=<your db host>
CH_USER=<your db user>
CH_PSW=<your db password>
REPLICATE_API_TOKEN=<your replicate api token>
YANDEX_API_KEY=<your yandex api-key>
YANDEX_FOLDER_ID=<your yandex folder id>
```

2. Then execute the commands in sequence:
```
make setup
source .venv/bin/activate
make run
```
