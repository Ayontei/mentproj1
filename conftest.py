import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Фикстура для DRF тестового клиента"""
    return APIClient()


@pytest.fixture
def user(db):
    """Создание обычного пользователя"""
    return baker.make(User, username="testuser", email="test@example.com")


@pytest.fixture
def admin_user(db):
    """Создание администратора"""
    return baker.make(User, username="admin", is_staff=True, is_superuser=True)


@pytest.fixture
def auth_client(api_client, user):
    """Клиент с авторизацией обычного пользователя"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Клиент с авторизацией админа"""
    api_client.force_authenticate(user=admin_user)
    return api_client
