FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Отключаем создание виртуального окружения внутри контейнера
ENV POETRY_VIRTUALENVS_CREATE=false

# Сразу копируем ВЕСЬ проект
WORKDIR /app
COPY . /app

# Теперь устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
