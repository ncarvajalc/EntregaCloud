#!/usr/bin/make

include .env

help:
	@echo "make"
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
