FROM python:3.8-alpine

MAINTAINER MDCG
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /opt/code/
WORKDIR /opt/code/

CMD ["python", "-m", "src.bot.core"]
