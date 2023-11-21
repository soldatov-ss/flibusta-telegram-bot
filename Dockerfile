FROM python:3.10

WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY requirements.txt /src
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 3306