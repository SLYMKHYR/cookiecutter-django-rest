SHELL := /bin/bash
GIT_SHA = $(shell git describe --tags --always)
GIT_BRANCH = $(shell git symbolic-ref --short -q HEAD)
BRANCH_VALID := $(shell [[ $(shell git symbolic-ref --short -q HEAD) =~ ^((TPPMD-)\/([0-9]*)|(develop|sandbox|alpha|staging|production))$$ ]] && echo matched)
TAG ?= v0.0.1
TAG_ESC := $(subst /,-,$(TAG))
TAG_ESC := $(subst \,-,$(TAG_ESC))
IMAGE_NAME = {{cookiecutter.app_name}}
REPO_URL = "Tamatem-Plus/$(IMAGE_NAME)"
DOCKER_IMAGE = $(REPO_URL):$(TAG_ESC)

all: image

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

image:			## Build docker images
	docker build -t current -t $(IMAGE_NAME) -t $(DOCKER_IMAGE) .

services:		## Build services images
	docker-compose -f ./compose.yaml -f ./compose.services.yaml build

push:			## Push docker images
	docker push $(DOCKER_IMAGE)

services-start:		## Creates necessary services for development in background
	docker-compose  -f ./compose.services.yaml up -d

services-stop:		## Stops services and removes services created by 'up'
	docker-compose  -f ./compose.services.yaml down

start:			## Run app locally in background
	docker-compose -f ./compose.yaml -f ./compose.services.yaml up -d

stop:			## Stops containers and removes containers, networks, volumes, and images created by 'up'
	docker-compose -f ./compose.yaml -f ./compose.services.yaml down

restart:		## Restart containers
	docker-compose -f ./compose.yaml -f ./compose.services.yaml restart

migrations:		## Creates Migrations
	docker-compose -f ./compose.yaml run --rm api makemigrations

migrate:		## Do migrations
	docker-compose -f ./compose.yaml run --rm api migrate

generate-trans:		## Generate translation files
	docker-compose -f ./compose.yaml exec api python manage.py makemessages --no-wrap --no-location --locale=ar

compile-trans:		## Compile translation files
	docker compose -f ./compose.yaml exec api python manage.py compilemessages --locale=ar

collect-static:		## Collect static files
	exec python manage.py collectstatic --noinput

tag:			## Check and return docker tag name
ifneq ($(BRANCH_VALID),matched)
	$(error Wrong branch name!)
endif
	@echo $(TAG_ESC)
