FROM python:3.11.3-slim-bullseye


RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/src/app/api

COPY requirements.txt /usr/src/app/api/requirements.txt

RUN pip install --upgrade pip \
    pip install -r /usr/src/app/api/requirements.txt

COPY . /usr/src/app/api
