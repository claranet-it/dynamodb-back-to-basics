.PHONY: help up down init-db logs status admin-ui install start-local test coverage lint lint-fix format

run-docker-compose = docker compose -f docker-compose.yml
server_port = 3000

default: help

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

up: # Start containers and tail logs
	$(run-docker-compose) up -d 

down: # Stop all containers
	$(run-docker-compose) down --remove-orphans

init-db: # Initialize the database and load fixtures
	$(run-docker-compose) --profile dev up -d 

logs: # Tail container logs
	$(run-docker-compose) logs -f dynamodb-local

status: # Show status of all containers
	$(run-docker-compose) ps

admin-ui: # Open the UI in the browser
	open http://localhost:8001

install: # Install dependencies
	poetry install
	cp .env.example .env

start-local: # Start the local server
	poetry run uvicorn app.main:app --reload --port $(server_port)

test: # Run tests
ifdef filter
	poetry run pytest $(filter) -vv
else
	poetry run pytest -vv
endif

coverage: test # Run tests with coverage
	poetry run pytest --cov-report term-missing --cov=app

lint: # Run linter
	poetry run ruff check .

lint-fix: # Run linter with fix
	poetry run ruff check --fix .

format: # Run formatter
	poetry run ruff format .