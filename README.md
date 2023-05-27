### Необходимые инструменты
- linux/macos
- Python 3.10
https://python.org
- poetry
https://python-poetry.org/docs/
- postgres

Можно установить по инструкции:

https://www.postgresql.org/download/

Можно через Docker командой:

`docker run --name service-db -e POSTGRES_DB=service -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 15432:5432 -d postgres`

Но тогда нужен докер:

https://docs.docker.com/engine/install/
## После установки инструментов
# Cклонировать проект:
git clone https://github.com/NeverEverLive/trans-region-system.git

# Скачать зависимости

`poetry install`

В файле .env:
Поставить значение в BUCKET_PATH - полный путь до проекта

# Запустить проект

```
poetry run python3 server.py
or
poetry run python server.py
```