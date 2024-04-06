#!/usr/bin/make

OS := $(shell uname -s)
VENV := .venv

help:
	@echo "make"
	@echo "    help"
	@echo "        Show this help."
	@echo "    setup"
	@echo "        Setup the project."
	@echo "    clean"
	@echo "    run-dev-build"
	@echo "        Run development docker compose and force build containers."
	@echo "    run-dev"
	@echo "        Run development docker compose."
	@echo "    stop-dev"
	@echo "        Stop development docker compose."
	@echo "    run-prod"
	@echo "        Run production docker compose."
	@echo "    stop-prod"
	@echo "        Stop production docker compose."		
setup:
ifeq ($(OS),Darwin) # macOS
	python3 -m venv $(VENV) && source $(VENV)/bin/activate && python -m pip install --upgrade pip && echo "POSTGRES_USER=postgres\nPOSTGRES_PASSWORD=postgres\nPOSTGRES_DB=cloud" > .env
else ifeq ($(OS),Linux)
	python3 -m venv $(VENV) && source $(VENV)/bin/activate && python -m pip install --upgrade pip && echo "POSTGRES_USER=postgres\nPOSTGRES_PASSWORD=postgres\nPOSTGRES_DB=cloud" > .env
else # Assuming Windows
	python -m venv $(VENV) && .\$(VENV)\Scripts\activate.bat && python -m pip install --upgrade pip && echo POSTGRES_USER=postgres > .env && echo POSTGRES_PASSWORD=postgres >> .env && echo POSTGRES_DB=cloud >> .env
endif
clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .tox
	rm -rf .env
run-dev-build:
	docker compose -f docker-compose-dev.yml up --build

run-dev:
	docker compose -f docker-compose-dev.yml up

stop-dev:
	docker compose -f docker-compose-dev.yml down

run-prod:
	docker compose up --build

stop-prod:
	docker compose down
