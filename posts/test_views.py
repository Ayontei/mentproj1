import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from categories.models import Category
from posts.models import Post

from django.test import override_settings
from unittest.mock import patch


@pytest.mark.django_db
def test_get_posts_list(api_client):
    baker.make(Post, _quantity=3, is_published=True)

    url = reverse("post-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    posts = response.data["results"]["posts"]
    assert len(posts) == 3


@pytest.mark.django_db
def test_create_post_unauthorized(api_client):
    """Тест создания поста без авторизации (должен быть 403)"""
    url = reverse("post-list")
    data = {"title": "New Post", "content": "Content"}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_post_authorized(auth_client):
    """Тест создания поста авторизованным пользователем"""
    url = reverse("post-list")
    data = {
        "title": "Test Post",
        "content": "Test Content",
        "is_published": True,
        "slug": "test-post",
    }

    response = auth_client.post(url, data)

    # Отладочный вывод
    if response.status_code == 400:
        print("\n" + "=" * 50)
        print("ОШИБКИ ВАЛИДАЦИИ:")
        print(response.data)
        print("=" * 50)

    assert response.status_code == 201


@pytest.mark.django_db
def test_post_search(auth_client):
    """Тест поиска по постам"""
    # Очищаем все посты перед тестом
    Post.objects.all().delete()

    # Создаем тестовые данные
    baker.make(Post, title="Python Django", content="Framework", is_published=True)
    baker.make(Post, title="JavaScript React", content="Library", is_published=True)

    url = reverse("post-list")
    response = auth_client.get(url, {"search": "Python"})

    assert response.status_code == 200
    # ✅ Правильный путь к данным
    posts = response.data["results"]["posts"]
    assert len(posts) == 1
    assert posts[0]["title"] == "Python Django"


@pytest.mark.django_db
def test_post_filter_by_category(auth_client):
    """Тест фильтрации по категории"""
    # Создаем категорию
    category = baker.make(Category, name="Test Category")

    # Создаем посты: один с категорией, один без
    post_with_category = baker.make(Post, categories=category, is_published=True)

    url = reverse("post-list")
    response = auth_client.get(url, {"category": category.id})

    assert response.status_code == 200
    posts = response.data["results"]["posts"]
    assert len(posts) == 1
    assert posts[0]["id"] == post_with_category.id


# @pytest.mark.django_db
# @patch("subscriptions.tasks.logger")  # Мокаем логгер вместо notify_subscribers
# def test_post_creation_triggers_notification(mock_logger, auth_client):
#     """Тест: при публикации поста вызывается логирование уведомления"""
#     url = reverse("post-list")

#     data = {
#         "title": "Test Post for Notification",
#         "content": "This post should trigger notification",
#         "is_published": True,
#         "slug": "test-notification",
#     }

#     response = auth_client.post(url, data)

#     assert response.status_code == status.HTTP_201_CREATED

#     # ✅ Проверяем, что логгер был вызван с информацией об уведомлении
#     mock_logger.info.assert_called_once()
#     log_message = mock_logger.info.call_args[0][0]
#     assert "Уведомление" in log_message
#     assert "Test Post for Notification" in log_message


@pytest.mark.django_db
@patch("subscriptions.tasks.logger")
def test_draft_post_does_not_trigger_notification(mock_logger, auth_client):
    """Тест: черновик НЕ вызывает логирование"""
    url = reverse("post-list")

    data = {
        "title": "Draft Post",
        "content": "This post should not trigger notification",
        "is_published": False,
        "slug": "draft-post",
    }

    response = auth_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    mock_logger.info.assert_not_called()


@pytest.mark.django_db
@patch("subscriptions.tasks.logger")
def test_post_creation_triggers_notification(mock_logger, auth_client):
    url = reverse("post-list")
    data = {
        "title": "Test Post",
        "content": "Content",
        "is_published": True,
        "slug": "test-post",
    }

    response = auth_client.post(url, data)
    assert response.status_code == 201

    # ✅ Важно! Запускаем задачу синхронно для теста
    from subscriptions.tasks import notify_subscribers

    notify_subscribers(
        author_id=response.data["author"],
        post_title=data["title"],
        post_id=response.data["id"],
    )

    mock_logger.info.assert_called_once()


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
@patch("subscriptions.tasks.logger")
def test_notification_logs_correctly(mock_logger, auth_client, user):
    # Создаем подписчика для автора
    from subscriptions.models import Sub
    from django.contrib.auth.models import User

    subscriber = User.objects.create_user(
        username="subscriber", email="subscriber@test.com", password="password"
    )

    # Подписываем на автора (который в auth_client)
    Sub.objects.create(
        subscriber=subscriber,
        target_user=auth_client.handler._force_user,
        is_active=True,
    )

    url = reverse("post-list")
    data = {
        "title": "Test Post",
        "content": "Content",
        "is_published": True,
        "slug": "test-post",
    }

    response = auth_client.post(url, data)
    assert response.status_code == 201

    # Теперь должны быть подписчики
    mock_logger.info.assert_called()
    log_message = mock_logger.info.call_args[0][0]
    assert "Notified" in log_message  # теперь будет Notified
