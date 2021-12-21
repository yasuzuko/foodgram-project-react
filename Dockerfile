FROM python:3-slim

WORKDIR /app

RUN python3 -m pip install -U pip setuptools wheel

COPY backend/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary-2.8.6

COPY . .

CMD gunicorn foodgram.wsgi -b 0.0.0.0:8000
