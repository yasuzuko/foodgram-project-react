FROM python:3-slim

WORKDIR /app

RUN python3 -m pip install -U pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# while dev
RUN python manage.py migrate
RUN python manage.py collectstatic
RUN python manage.py load_data

# CMD gunicorn foodgram.wsgi -b 0.0.0.0:8000
CMD python manage.py runserver 0.0.0.0:8000