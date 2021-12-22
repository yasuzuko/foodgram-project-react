# Дипломный проект Foodgram

![Foodgram workflow](https://github.com/yasuzuko/yamdb_finfoodgram-project-react/actions/workflows/main.yml/badge.svg)


## Описание проекта

Foodgram, «Продуктовый помощник», онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Спецификация api

Спецификация api представлена в документации: http://<здесь будет ссылка>

## Установка и запуск
### Подготовка
После клонирования репозитория необходимо заполнить GitHub Secrets
SSH_SERVER = ip-адрес сервера, на котором будет развернут проект
SSH_USER, SSH_KEY, SSH_PASSPHRASE - параметры доступа по SSH 
DOCKER_USERNAME = имя репозитория DockerHub
DOCKER_PASSWORD = пароль для репозитория DockerHub
SECRET_KEY = переменная окружения SECRET_KEY, из настроек Django
POSTGRES_DB = foodgram_db, имя БД
POSTGRES_USER = имя_пользователя_postgres
POSTGRES_PASSWORD = пароль_пользователя_postgres
DB_HOST = db, название контейнера, на котором развернута БД
DB_PORT = 5432
TELEGRAM_TO, TELEGRAM_TOKEN - параметры контакта для отправки сообщения в телеграм

на удаленном сервере SSH_SERVER должен быть установлен Docker и docker-compose

### Деплой
для запуска деплоя на сервер должен сработать GitHub workflow
- проверит код с помощью flake8
- создаст образ контейнера backend (django+gunicorn) и загрузит его на DockerHub
- подключится к удаленному SSH_SERVER и загрузит образы backend, frontend,

для запуска контейнеров подключиться к серверу по SSH и запустить docker-compose
docker-compose up -d

в файле docker-compose.yml описан запуск контейнеров db, backend, frontend, nginx

### Начальная настройка
подключиться по SSH к серверу и зайти в контейнер backend, выполнить команды:
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser - добавить администратора Django
python manage.py load_data - команда загрузит первоначальный список доступных ингредиентов для рецептов в БД
python manage.py loaddata fixtures.json - команда загрузит тестовый набор данных

В тестовом режиме проект доступен по адресу http://62.84.112.164