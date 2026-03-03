# MentProj API

Платформа для публикации постов с системой подписок и уведомлений. Проект построен на Django REST Framework с использованием JWT-аутентификации, Celery для асинхронных задач и Docker для контейнеризации.

## ✨ Возможности

- 📝 Публикация постов с категориями и тегами
- 🔐 JWT-аутентификация (access/refresh токены)
- 👥 Подписка на других пользователей
- 📧 Асинхронные уведомления подписчиков (Celery + RabbitMQ)
- 🔍 Поиск, фильтрация и сортировка постов
- 📚 Автоматическая документация OpenAPI (Swagger/ReDoc)
- 🐳 Полная контейнеризация через Docker
- ✅ Линтеры (ruff, mypy,) через pre-commit
- 🧪 Тесты с pytest

## 🚀 Быстрый старт

### Предварительные требования

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта

```bash
# Клонировать репозиторий
git clone <url-репозитория>
cd mentproj

# Запустить контейнеры
docker-compose up -d


### Применить миграции

```bash
# Внутри контейнера
docker exec -it mentproj-web-1 python manage.py migrate


### Создать суперпользователя

```bash
# Интерактивно
docker exec -it mentproj-web-1 python manage.py createsuperuser

### Остановка проекта

```bash
docker-compose down


## 📚 Документация API

После запуска проекта документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## 🧪 Линтеры и тесты

### Запуск линтеров

```bash
# Проверить код линтерами
pre-commit run --all-files

# Запустить только ruff
docker exec mentproj-web-1 ruff check .

# Запустить только mypy
docker exec mentproj-web-1 mypy .
```

### Запуск тестов

```bash
# Все тесты
docker exec mentproj-web-1 pytest

# С подробным выводом
docker exec mentproj-web-1 pytest -v

# С отчетом о покрытии
docker exec mentproj-web-1 pytest --cov=posts --cov-report=html
```

## 🐳 Команды Docker

### Основные команды

```bash
# Собрать и запустить
docker-compose up -d --build

# Посмотреть логи
docker-compose logs -f

# Остановить
docker-compose down

# Остановить с удалением томов (очистить БД)
docker-compose down -v

# Зайти в контейнер
docker exec -it mentproj-web-1 bash
```

## 📁 Структура проекта

```
mentproj/
├── categories/          # Приложение категорий
├── posts/               # Приложение постов
├── subscriptions/       # Приложение подписок и уведомлений
├── tags/                # Приложение тегов
├── users/               # Приложение пользователей
├── ment/                # Основные настройки проекта
├── .env/                # Виртуальное окружение
├── .pre-commit-config.yaml  # Конфигурация pre-commit
├── docker-compose.yml   # Конфигурация Docker
├── Dockerfile           # Dockerfile для сборки
├── pytest.ini           # Настройки pytest
├── pyproject.toml       # Зависимости (Poetry)
└── README.md            # Этот файл
```

## 🛠️ Используемые технологии

- **Django 6.0.2** + **Django REST Framework**
- **PostgreSQL** — база данных
- **JWT** — аутентификация (djangorestframework-simplejwt)
- **Celery** + **RabbitMQ** — асинхронные задачи
- **Docker** + **Docker Compose** — контейнеризация
- **pytest** + **model-bakery** — тестирование
- **ruff**, **mypy** — линтеры и форматтеры
- **pre-commit** — хуки для проверки кода
- **drf-yasg** — OpenAPI документация
