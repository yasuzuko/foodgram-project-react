FROM python:3-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

WORKDIR /app

RUN python3 -m pip install -U pip setuptools wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN ls

CMD gunicorn foodgram.wsgi -b 0.0.0.0:8000
