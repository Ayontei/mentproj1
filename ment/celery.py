import os

from celery import Celery

# Установите модуль настроек Django по умолчанию
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ment.settings")

app = Celery("ment")

# Используйте строку конфига, чтобы не передавать объект напрямую
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находите задачи во всех установленных приложениях
app.autodiscover_tasks()
