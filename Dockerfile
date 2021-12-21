FROM python:3-slim

WORKDIR /app

RUN python3 -m pip install -U pip

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn foodgram.wsgi -b 0.0.0.0:8000
