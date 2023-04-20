FROM python:3.10-slim

RUN apt-get --yes update &&\
    apt-get --yes install libopenblas-dev libomp-dev build-essential curl git

ENV PATH="${PATH}:${HOME}/.local/bin"

COPY /src /app/src
COPY poetry.lock pyproject.toml README.md .env /app/

WORKDIR /app

RUN pip install --upgrade pip && pip install setuptools && pip install poetry \
    && poetry build \
    && pip install ./dist/*.tar.gz
