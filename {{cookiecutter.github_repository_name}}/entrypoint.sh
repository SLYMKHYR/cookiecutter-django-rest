#!/bin/bash
set -x
action=$1
shift

ENVIRONMENT=${ENVIRONMENT:-local}

case $action in
  runserver)
    (poetry run python manage.py migrate || exit 1 ) && poetry run python manage.py runserver 0.0.0.0:8000
    ;;
  gunicorn)
    (python manage.py migrate || exit 1 ) && gunicorn --workers=5 --timeout 60 {{cookiecutter.app_name}}.wsgi:application -b 0.0.0.0:8000 -k gevent
    ;;
  test)
    (poetry install && poetry run coverage run manage.py test || exit 1 ) && poetry run coverage report -m
    ;;
  celery)
    exec celery -A {{cookiecutter.app_name}}.celery worker -l INFO "$@"
    ;;
  celery-beat)
    exec celery -A {{cookiecutter.app_name}}.celery beat -l INFO "$@"
    ;;
  makemigrations)
    poetry run python manage.py makemigrations
    ;;
  migrate)
    poetry run python manage.py migrate
    ;;
  *)
    poetry run python manage.py runserver 0.0.0.0:8000
    ;;
esac