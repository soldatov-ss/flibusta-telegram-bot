FROM python:3.11.9-slim-bullseye


RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/bot

COPY requirements.txt /usr/src/app/bot

RUN pip install --upgrade pip \
    && pip install -r /usr/src/app/bot/requirements.txt

COPY . /usr/src/app/bot
