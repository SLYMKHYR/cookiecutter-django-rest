FROM python:3.12.4-slim as base

# Allows docker to cache installed dependencies between builds
RUN apt-get update && apt-get -y install libpq-dev gcc gettext xmlsec1
RUN pip3 install --upgrade pip poetry==2.0.1 gevent==24.11.1

# Security Context 
RUN useradd -m nonroot
USER nonroot

COPY . /app
WORKDIR app
RUN poetry config virtualenvs.create false && poetry install
RUN chmod a+x /app/entrypoint.sh
RUN python manage.py collectstatic --no-input

EXPOSE 8000
# Run the production server
ENTRYPOINT ./entrypoint.sh
