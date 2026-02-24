# Makefile для Django проекта

.PHONY: help run migrate makemigrations shell test clean

# Цвета для вывода
YELLOW := \033[33m
RESET := \033[0m

help:
	@echo "$(YELLOW)Available commands:$(RESET)"
	@echo "  make run              - Run development server"
	@echo "  make migrate          - Apply migrations"
	@echo "  make makemigrations   - Create new migrations"
	@echo "  make shell            - Open Django shell"
	@echo "  make test             - Run tests"
	@echo "  make clean            - Clean cache files"
	@echo "  make superuser        - Create superuser"

run:
	.env\Scripts\python manage.py runserver

migrate:
	.env\Scripts\python manage.py migrate

makemigrations:
	.env\Scripts\python manage.py makemigrations

shell:
	.env\Scripts\python manage.py shell

test:
	pytest

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete
	rm -rf .pytest_cache .coverage htmlcov

superuser:
	.env\Scripts\python manage.py createsuperuser
