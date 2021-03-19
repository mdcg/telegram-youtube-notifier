FROM python:3.8-alpine

MAINTAINER MDCG
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /opt/code/
WORKDIR /opt/code/

