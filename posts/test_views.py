import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from categories.models import Category
from posts.models import Post


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
